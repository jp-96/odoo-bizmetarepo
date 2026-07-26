from odoo import models, fields, api
import zlib
import base64
import requests
import logging
_logger = logging.getLogger(__name__)

# PlantUML の 64 文字セット
plantuml_alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"

def _encode_6bit(b):
    return plantuml_alphabet[b & 0x3F]

def _append_3bytes(b1, b2, b3):
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    return (
        _encode_6bit(c1)
        + _encode_6bit(c2)
        + _encode_6bit(c3)
        + _encode_6bit(c4)
    )

def plantuml_encode(text):
    # zlib 圧縮（PlantUML 仕様）
    zlibbed = zlib.compress(text.encode("utf-8"))
    data = zlibbed[2:-4]  # ヘッダとフッタを除去

    res = []
    for i in range(0, len(data), 3):
        b1 = data[i]
        b2 = data[i + 1] if i + 1 < len(data) else 0
        b3 = data[i + 2] if i + 2 < len(data) else 0
        res.append(_append_3bytes(b1, b2, b3))

    return "".join(res)


class UmlGenerator(models.TransientModel):
    _name = "ems.cdm.uml_generator"
    _description = "ems.cdm UML Generator"

    uml_text = fields.Text(string="UML（編集可能）")
    uml_png_url = fields.Char(string="PNG URL")
    uml_png = fields.Binary(string="UML PNG")

    # generate_note = fields.Boolean(string="ルールノートを出力する", default=True)

    # ---------------------------------------------------------
    # 初回 UML 生成
    # ---------------------------------------------------------
    def generate_uml(self):
        Entities = self.env["ems.cdm.entity"].search([])
        Attributes = self.env["ems.cdm.attribute"].search([])
        Domains = self.env["ems.cdm.attribute_domain"].search([])
        References = self.env["ems.cdm.entity_reference"].search([])
        Rules = self.env["ems.cdm.rule"].search([])

        lines = []
        lines.append("@startuml")
        # lines.append("skinparam classAttributeIconSize 0")

        # ---------------------------------------------------------
        # クラス定義
        # ---------------------------------------------------------
        for entity in Entities:
            if entity.subject_area_id:
                entity_name = f"{entity.subject_area_id.name}.{entity.name}"
            else:
                entity_name = entity.name

            lines.append(f'entity "{entity_name}" {{')

            # 属性
            entity_attributes = Attributes.filtered(lambda i: i.entity_id.id == entity.id)
            for attribute in entity_attributes:
                domain = attribute.domain_id
                if domain:
                    if domain.data_type == "extended":
                        pass
                    elif domain.data_type == "relation":
                        lines.append(f'  {attribute.name} <FK>')
                    elif domain.data_type == "reference":
                        pass
                    else:
                        domain_name = domain.name if domain else "Unknown"
                        lines.append(f'  {attribute.name} : {domain_name}')
                else:
                    lines.append(f'  {attribute.name}')

            # ルール
            for rule in Rules:
                if rule.entity_id.id != entity.id:
                    continue  # 代表エンティティ以外には追加しない

                # ---------------------------------------------------------
                # メソッド引数の生成
                # ---------------------------------------------------------
                targets = rule.target_attribute_ids
                args = []

                for target in targets:
                    attr = target.attribute_id
                    attr_entity = attr.entity_id

                    # 属性の修飾名を決定
                    if attr_entity.id == entity.id:
                        # 代表エンティティの属性 → 修飾なし
                        arg_name = attr.name
                    else:
                        # 別エンティティの属性 → エンティティ名で修飾
                        if attr_entity.subject_area_id and attr_entity.subject_area_id.id != entity.subject_area_id.id:
                            arg_name = f"{attr_entity.subject_area_id.name}.{attr_entity.name}.{attr.name}"
                        else:
                            arg_name = f"{attr_entity.name}.{attr.name}"

                    args.append(arg_name)

                # 引数リストをカンマ区切りに
                args_text = ", ".join(args)

                # ---------------------------------------------------------
                # メソッド追加
                # ---------------------------------------------------------
                lines.append(f'  - {rule.name}({args_text})')



            lines.append("}")

        # ---------------------------------------------------------
        # attribute_domain によるリンクを出力
        # ここで出力した entity ペアを記録する
        # ---------------------------------------------------------
        linked_pairs = set()

        for domain in Domains:
            if not domain.relation_entity_id:
                continue

            used_attributes = Attributes.filtered(lambda i: i.domain_id.id == domain.id)

            for attribute in used_attributes:
                left_entity = domain.relation_entity_id
                right_entity = attribute.entity_id

                if left_entity.subject_area_id:
                    left = f"{left_entity.subject_area_id.name}.{left_entity.name}"
                else:
                    left = left_entity.name

                if right_entity.subject_area_id:
                    right = f"{right_entity.subject_area_id.name}.{right_entity.name}"
                else:
                    right = right_entity.name

                # 記録用ペア
                pair = (left, right)

                if domain.data_type == "extended":
                    lines.append(f'"{left}" <|-- "{right}"')
                    linked_pairs.add(pair)

                elif domain.data_type == "relation":
                    label = attribute.name
                    lines.append(f'"{left}" --{{ "{right}" : "{label}"')
                    linked_pairs.add(pair)

                # reference は出力しない
                elif domain.data_type == "reference":
                    pass

        # ---------------------------------------------------------
        # EntityReference の参照リンクを出力
        # ただし attribute_domain で既にリンクがある場合は出力しない
        # ---------------------------------------------------------
        for ref in References:
            left_entity = ref.target_entity_id
            right_entity = ref.source_entity_id

            if left_entity.subject_area_id:
                left = f"{left_entity.subject_area_id.name}.{left_entity.name}"
            else:
                left = left_entity.name

            if right_entity.subject_area_id:
                right = f"{right_entity.subject_area_id.name}.{right_entity.name}"
            else:
                right = right_entity.name

            pair = (left, right)

            # ★ attribute_domain で既にリンクがある場合は出力しない
            if pair in linked_pairs:
                continue

            lines.append(f'"{left}" <.. "{right}"')

        # ---------------------------------------------------------
        # ルール（cdm.rule）を note として出力
        # ---------------------------------------------------------
        generate_note = self.env.context.get('generate_note', True)
        if generate_note:
            rule_counter = 0
            for rule in Rules:
                rule_counter += 1

                # note の追加（別名）
                note_name = f"note{rule_counter:03d}"
                note_body = f"{rule.name}\n{rule.description}"
                note = f'note "{note_body}" as {note_name}'.replace("\n", "\\n")

                entity = rule.entity_id
                subject_area = entity.subject_area_id
                if subject_area:
                    # package で note を囲む
                    lines.append(f'package "{subject_area.name}" {{')
                    lines.append(f"   {note}")
                    lines.append("}")
                    # ダミーリンク
                    entity_name = f"{subject_area.name}.{entity.name}"
                else:
                    # 通常 note
                    lines.append(note)
                    # ダミーリンク
                    entity_name = f"{entity.name}"

                # 隠しリンク（吹き出しではなく、線にするため）
                lines.append(f'{entity_name} .[hidden]. "{note_name}" : "(dummy link)"')

                # -----------------------------------------------------
                # note のリンク先エンティティを決定
                # -----------------------------------------------------
                targets = rule.target_attribute_ids

                if not targets:
                    # RuleTarget が 0件 → rule.entity_id のみ
                    entity_list = [rule.entity_id]
                else:
                    # RuleTarget が 1件以上 → target_attribute_ids の entity 全て
                    entity_list = list({
                        attr.attribute_id.entity_id
                        for attr in targets
                        if attr.attribute_id
                    })

                # -----------------------------------------------------
                # ★ note は複数エンティティにリンクできる
                # ★ ただし同一エンティティへのリンクは 1 回のみ
                # -----------------------------------------------------
                note_entity_links = set()
                for entity in entity_list:
                    if entity.subject_area_id:
                        entity_name = f"{entity.subject_area_id.name}.{entity.name}"
                    else:
                        entity_name = entity.name

                    link_key = (note_name, entity_name)
                    
                    if link_key not in note_entity_links:
                        lines.append(f'{entity_name} .. "{note_name}" : "{rule.name}"')
                        note_entity_links.add(link_key)

        lines.append("@enduml")

        uml_text = "\n".join(lines)
        self.uml_text = uml_text

        encoded = plantuml_encode(uml_text)
        url = f"https://www.plantuml.com/plantuml/png/{encoded}"
        self.uml_png_url = url

        response = requests.get(url)
        _logger.warning("PlantUML status = %s", response.status_code)
        if response.status_code == 200:
            self.uml_png = base64.b64encode(response.content)
        else:
            self.uml_png = False

        return {
            "type": "ir.actions.act_window",
            "res_model": "ems.cdm.uml_generator",
            "view_mode": "form",
            "target": "new",
            "res_id": self.id,
        }

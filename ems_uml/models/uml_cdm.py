from odoo import models
from .uml_base import BaseUmlGenerator

class CdmUmlGenerator(BaseUmlGenerator):
    _name = "ems.uml.cdm_generator"
    _description = "CDM UML Generator"

    def build_uml_lines(self):
        lines = []

        Entities = self.env["ems.cdm.entity"].search([])
        Attributes = self.env["ems.cdm.attribute"].search([])
        Domains = self.env["ems.cdm.attribute_domain"].search([])
        References = self.env["ems.cdm.entity_reference"].search([])
        Rules = self.env["ems.cdm.rule"].search([])

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
        return lines

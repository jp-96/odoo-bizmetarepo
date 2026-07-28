from odoo import models
from .uml_base import BaseUmlGenerator

class LdmUmlGenerator(BaseUmlGenerator):
    _name = "ems.uml.ldm_generator"
    _description = "LDM UML Generator"

    def build_uml_lines(self):
        lines = []

        ObjectClasses = self.env["ems.ldm.object_class"].search([])
        DataElements = self.env["ems.ldm.data_element"].search([])
        Domains = self.env["ems.ldm.value_domain"].search([])
        # References = self.env["ems.cdm.entity_reference"].search([])
        Constraints = self.env["ems.ldm.constraint"].search([])

        lines.append("@startuml")
        # lines.append("skinparam classAttributeIconSize 0")

        # ---------------------------------------------------------
        # オブジェクトクラス
        # ---------------------------------------------------------
        for oc in ObjectClasses:
            if oc.system_id:
                oc_name = f"{oc.system_id.name}.{oc.name}"
            else:
                oc_name = oc.name

            lines.append(f'entity "{oc_name}" {{')

            # データ要素
            oc_elements = DataElements.filtered(lambda d: d.object_class_id.id == oc.id)
            for de in oc_elements:
                domain = de.value_domain_id
                if domain:
                    if domain.data_type == "extended":
                        pass
                    elif domain.data_type == "relation":
                        lines.append(f'  {de.name} <FK>')
                    else:
                        domain_name = domain.name if domain else "Unknown"
                        lines.append(f'  {de.name} : {domain_name}')
                else:
                    lines.append(f'  {de.name}')

            # 制約
            for constraint in Constraints:
                if constraint.object_class_id.id != oc.id:
                    continue  # 代表のオブジェクトクラス以外には追加しない

                # ---------------------------------------------------------
                # メソッド引数の生成
                # ---------------------------------------------------------
                targets = constraint.target_ids
                args = []

                for target in targets:
                    de = target.data_element_id
                    de_oc = de.object_class_id

                    # データ要素の修飾名を決定
                    if de_oc.id == oc.id:
                        # 代表のオブジェクトクラスのデータ要素 → 修飾なし
                        arg_name = de.name
                    else:
                        # 別オブジェクトクラスのデータ要素 → オブジェクトクラス名で修飾
                        if de_oc.system_id and de_oc.system_id.id != oc.system_id.id:
                            arg_name = f"{de_oc.system_id.name}.{de_oc.name}.{de.name}"
                        else:
                            arg_name = f"{de_oc.name}.{de.name}"

                    args.append(arg_name)

                # 引数リストをカンマ区切りに
                args_text = ", ".join(args)

                # ---------------------------------------------------------
                # メソッド追加
                # ---------------------------------------------------------
                lines.append(f'  - {constraint.name}({args_text})')



            lines.append("}")

        # ---------------------------------------------------------
        # attribute_domain によるリンクを出力
        # ここで出力した entity ペアを記録する
        # ---------------------------------------------------------
        linked_pairs = set()

        for domain in Domains:
            if not domain.relation_object_class_id:
                continue

            used_elements = DataElements.filtered(lambda i: i.value_domain_id.id == domain.id)

            for de in used_elements:
                left_oc = domain.relation_object_class_id
                right_oc = de.object_class_id

                if left_oc.system_id:
                    left = f"{left_oc.system_id.name}.{left_oc.name}"
                else:
                    left = left_oc.name

                if right_oc.system_id:
                    right = f"{right_oc.system_id.name}.{right_oc.name}"
                else:
                    right = right_oc.name

                # 記録用ペア
                pair = (left, right)

                if domain.data_type == "extended":
                    lines.append(f'"{left}" <|-- "{right}"')
                    linked_pairs.add(pair)

                elif domain.data_type == "relation":
                    label = de.name
                    lines.append(f'"{left}" --{{ "{right}" : "{label}"')
                    linked_pairs.add(pair)

        # ---------------------------------------------------------
        # 制約（ldm.constraint）を note として出力
        # ---------------------------------------------------------
        generate_note = self.env.context.get('generate_note', True)
        if generate_note:
            note_counter = 0
            for constraint in Constraints:
                note_counter += 1

                # note の追加（別名）
                note_name = f"note{note_counter:03d}"
                note_body = f"{constraint.name}\n{constraint.description}"
                note = f'note "{note_body}" as {note_name}'.replace("\n", "\\n")

                oc = constraint.object_class_id
                oc_system = oc.system_id
                if oc_system:
                    # package で note を囲む
                    lines.append(f'package "{oc_system.name}" {{')
                    lines.append(f"   {note}")
                    lines.append("}")
                    # ダミーリンク
                    oc_name = f"{oc_system.name}.{oc.name}"
                else:
                    # 通常 note
                    lines.append(note)
                    # ダミーリンク
                    oc_name = f"{oc.name}"

                # 隠しリンク（吹き出しではなく、線にするため）
                lines.append(f'{oc_name} .[hidden]. "{note_name}" : "(dummy link)"')

                # -----------------------------------------------------
                # note のリンク先オブジェクトクラスを決定
                # -----------------------------------------------------
                targets = constraint.target_ids

                if not targets:
                    # 対象 が 0件 → constraint.object_class_id のみ
                    oc_list = [constraint.object_class_id]
                else:
                    # 対象 が 1件以上 → target_ids の entity 全て
                    oc_list = list({
                        target.data_element_id.object_class_id
                        for target in targets
                        if target.data_element_id
                    })

                # -----------------------------------------------------
                # ★ note は複数オブジェクトクラスにリンクできる
                # ★ ただし同一オブジェクトクラスへのリンクは 1 回のみ
                # -----------------------------------------------------
                note_links = set()
                for oc in oc_list:
                    if oc.system_id:
                        oc_name = f"{oc.system_id.name}.{oc.name}"
                    else:
                        oc_name = oc.name

                    link_key = (note_name, oc_name)
                    
                    if link_key not in note_links:
                        lines.append(f'{oc_name} .. "{note_name}" : "{constraint.name}"')
                        note_links.add(link_key)

        lines.append("@enduml")
        return lines

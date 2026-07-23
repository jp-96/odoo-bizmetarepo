from odoo import models, fields, api

class UmlGenerator(models.TransientModel):
    _name = "ems.cdm.uml_generator"
    _description = "ems.cdm UML Generator"

    uml_text = fields.Text(string="UML")

    def generate_uml(self):
        Entities = self.env["ems.cdm.entity"].search([])
        Attributes = self.env["ems.cdm.attribute"].search([])
        Domains = self.env["ems.cdm.attribute_domain"].search([])
        References = self.env["ems.cdm.entity_reference"].search([])

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
            left_entity = ref.source_entity_id
            right_entity = ref.target_entity_id

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

            # 点線矢印（reference）
            lines.append(f'"{left}" ..> "{right}"')

        lines.append("@enduml")

        self.uml_text = "\n".join(lines)

        return {
            "type": "ir.actions.act_window",
            "res_model": "ems.cdm.uml_generator",
            "view_mode": "form",
            "target": "new",
            "res_id": self.id,
        }

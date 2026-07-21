from odoo import models, fields, api

class UmlGenerator(models.TransientModel):
    _name = "ems.cdm.uml_generator"
    _description = "ems.cdm UML Generator"

    uml_text = fields.Text(string="UML")

    def generate_uml(self):
        Entities = self.env["ems.cdm.entity"].search([])
        Attributes = self.env["ems.cdm.attribute"].search([])
        Domains = self.env["ems.cdm.attribute_domain"].search([])

        lines = []
        lines.append("@startuml")
        # lines.append("skinparam classAttributeIconSize 0")

        # ---------------------------------------------------------
        # クラス定義：entity のみ
        # ---------------------------------------------------------
        for entity in Entities:

            # subject_area.name + "." + entity.name
            if entity.subject_area_id:
                entity_name = f"{entity.subject_area_id.name}.{entity.name}"
            else:
                entity_name = entity.name

            lines.append(f'entity "{entity_name}" {{')

            # attribute を属性として出力
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
        # attribute_domain の参照先に応じてクラス同士をリンク
        # ---------------------------------------------------------
        for domain in Domains:
            if not domain.relation_entity_id:
                continue

            # この attribute_domain を使っている attribute をすべて取得
            used_attributes = Attributes.filtered(lambda i: i.domain_id.id == domain.id)

            for attribute in used_attributes:
                left_entity = domain.relation_entity_id
                right_entity = attribute.entity_id

                # subject_area.name + "." + entity.name
                if left_entity.subject_area_id:
                    left = f"{left_entity.subject_area_id.name}.{left_entity.name}"
                else:
                    left = left_entity.name

                if right_entity.subject_area_id:
                    right = f"{right_entity.subject_area_id.name}.{right_entity.name}"
                else:
                    right = right_entity.name

                if domain.data_type == "extended":
                    symbol = "<|--"
                    lines.append(f'"{left}" {symbol} "{right}"')
                elif domain.data_type == "relation":
                    symbol = "--{"
                    label = attribute.name
                    lines.append(f'"{left}" {symbol} "{right}" : "{label}"')
                elif domain.data_type == "reference":
                    symbol = "<.."
                    lines.append(f'"{left}" {symbol} "{right}"')
                

        lines.append("@enduml")

        self.uml_text = "\n".join(lines)

        return {
            "type": "ir.actions.act_window",
            "res_model": "ems.cdm.uml_generator",
            "view_mode": "form",
            "target": "new",
            "res_id": self.id,
        }

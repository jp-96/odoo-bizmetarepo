from odoo import models, fields, api

class UmlGenerator(models.TransientModel):
    _name = "ems.cdm.uml_generator"
    _description = "ems.cdm UML Generator"

    uml_text = fields.Text(string="UML")

    def generate_uml(self):
        Models = self.env["ems.cdm.entity"].search([])
        Items = self.env["ems.cdm.attribute"].search([])
        Domains = self.env["ems.cdm.attribute_domain"].search([])

        lines = []
        lines.append("@startuml")
        lines.append("skinparam classAttributeIconSize 0")

        # ---------------------------------------------------------
        # クラス定義：entity のみ
        # ---------------------------------------------------------
        for m in Models:

            # subject_area.name + "." + entity.name
            if m.subject_area_id:
                class_name = f"{m.subject_area_id.name}.{m.name}"
            else:
                class_name = m.name

            lines.append(f'class "{class_name}" {{')

            # attribute を属性として出力
            model_items = Items.filtered(lambda i: i.entity_id.id == m.id)
            for item in model_items:
                domain = item.domain_id
                domain_name = domain.name if domain else "Unknown"
                lines.append(f'  "{item.name}" : "{domain_name}"')

            lines.append("}")

        # ---------------------------------------------------------
        # attribute_domain の参照先に応じてクラス同士をリンク
        # ---------------------------------------------------------
        for d in Domains:
            if not d.relation_entity_id:
                continue

            # この attribute_domain を使っている attribute をすべて取得
            used_items = Items.filtered(lambda i: i.domain_id.id == d.id)

            for item in used_items:
                src_entity = d.relation_entity_id
                dst_entity = item.entity_id

                # subject_area.name + "." + entity.name
                if src_entity.subject_area_id:
                    src = f"{src_entity.subject_area_id.name}.{src_entity.name}"
                else:
                    src = src_entity.name

                if dst_entity.subject_area_id:
                    dst = f"{dst_entity.subject_area_id.name}.{dst_entity.name}"
                else:
                    dst = dst_entity.name

                if d.data_type == "extended":
                    lines.append(f'"{src}" <|-- "{dst}" : 継承')

                elif d.data_type == "relation":
                    lines.append(f'"{src}" --* "{dst}" : 関連')

                elif d.data_type == "reference":
                    lines.append(f'"{src}" <.. "{dst}" : 参照')

        lines.append("@enduml")

        self.uml_text = "\n".join(lines)

        return {
            "type": "ir.actions.act_window",
            "res_model": "ems.cdm.uml_generator",
            "view_mode": "form",
            "target": "new",
            "res_id": self.id,
        }

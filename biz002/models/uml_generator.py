from odoo import models, fields, api

class UmlGenerator(models.TransientModel):
    _name = "biz002.uml_generator"
    _description = "biz002 UML Generator"

    uml_text = fields.Text(string="UML")

    def generate_uml_old1(self):
        Models = self.env["biz002.data_model"].search([])
        Items = self.env["biz002.data_item"].search([])
        Domains = self.env["biz002.data_domain"].search([])

        lines = []
        lines.append("@startuml")
        lines.append("skinparam classAttributeIconSize 0")

        # ---------------------------------------------------------
        # クラス定義（すべて "" で囲む）
        # ---------------------------------------------------------

        for m in Models:
            lines.append(f'class "{m.name}" {{')
            lines.append("  + type : DataModel")
            lines.append("}")

        for i in Items:
            lines.append(f'class "{i.name}" {{')
            lines.append("  + type : DataItem")
            lines.append(f"  + required : {i.required}")
            lines.append("}")

        for d in Domains:
            lines.append(f'class "{d.name}" {{')
            lines.append("  + type : DataDomain")
            lines.append(f"  + data_type : {d.data_type}")
            if d.relation_model_id:
                lines.append(f'  + relation_model : "{d.relation_model_id.name}"')
            lines.append("}")

        # ---------------------------------------------------------
        # 結合（relation）: *--
        # ---------------------------------------------------------
        for i in Items:
            lines.append(f'"{i.model_id.name}" *-- "{i.name}" : 結合')
            lines.append(f'"{i.name}" *-- "{i.domain_id.name}" : 結合')

        # ---------------------------------------------------------
        # 派生（extended）: --|>
        # ---------------------------------------------------------
        for d in Domains:
            if d.data_type == "extended" and d.relation_model_id:
                lines.append(
                    f'"{d.name}" --|> "{d.relation_model_id.name}" : 派生'
                )

        # ---------------------------------------------------------
        # 依存（reference）: ..>
        # ---------------------------------------------------------
        for d in Domains:
            if d.data_type == "reference" and d.relation_model_id:
                lines.append(
                    f'"{d.name}" ..> "{d.relation_model_id.name}" : 依存'
                )

        lines.append("@enduml")

        self.uml_text = "\n".join(lines)

        return {
            "type": "ir.actions.act_window",
            "res_model": "biz002.uml_generator",
            "view_mode": "form",
            "target": "new",
            "res_id": self.id,
        }

    def generate_uml(self):
        Models = self.env["biz002.data_model"].search([])
        Items = self.env["biz002.data_item"].search([])
        Domains = self.env["biz002.data_domain"].search([])

        lines = []
        lines.append("@startuml")
        lines.append("skinparam classAttributeIconSize 0")

        # ---------------------------------------------------------
        # クラス定義：data_model のみ
        # ---------------------------------------------------------
        for m in Models:
            lines.append(f'class "{m.name}" {{')

            # data_item を属性として出力
            model_items = Items.filtered(lambda i: i.model_id.id == m.id)
            for item in model_items:
                domain = item.domain_id
                domain_name = domain.name if domain else "Unknown"
                lines.append(f'  "{item.name}" : "{domain_name}"')

            lines.append("}")

        # ---------------------------------------------------------
        # data_domain の参照先に応じてクラス同士をリンク
        # ---------------------------------------------------------
        for d in Domains:
            if not d.relation_model_id:
                continue

            # この data_domain を使っている data_item をすべて取得
            used_items = Items.filtered(lambda i: i.domain_id.id == d.id)

            for item in used_items:
                src = d.relation_model_id.name
                dst = item.model_id.name

                if d.data_type == "relation":
                    lines.append(f'"{src}" --* "{dst}" : 結合')

                elif d.data_type == "extended":
                    lines.append(f'"{src}" <|-- "{dst}" : 派生')

                elif d.data_type == "reference":
                    lines.append(f'"{src}" <.. "{dst}" : 依存')

        lines.append("@enduml")

        self.uml_text = "\n".join(lines)

        return {
            "type": "ir.actions.act_window",
            "res_model": "biz002.uml_generator",
            "view_mode": "form",
            "target": "new",
            "res_id": self.id,
        }

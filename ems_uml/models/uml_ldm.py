from odoo import models
from .uml_base import BaseUmlGenerator

class LdmUmlGenerator(BaseUmlGenerator):
    _name = "ems.uml.ldm_generator"
    _description = "LDM UML Generator"

    def build_uml_lines(self):
        lines = []

        ObjectClasses = self.env["ems.ldm.object_class"].search([])
        DataElements = self.env["ems.ldm.data_element"].search([])
        Constraints = self.env["ems.ldm.constraint"].search([])
        ConstraintTargets = self.env["ems.ldm.constraint_target"].search([])

        lines.append("@startuml")

        # ---------------------------------------------------------
        # ObjectClass を entity として出力
        # ---------------------------------------------------------
        for oc in ObjectClasses:
            if oc.system_id:
                entity_name = f"{oc.system_id.name}.{oc.name}"
            else:
                entity_name = oc.name

            lines.append(f'entity "{entity_name}" {{')

            # DataElement を属性として出力
            oc_elements = DataElements.filtered(lambda d: d.object_class_id.id == oc.id)
            for de in oc_elements:
                domain = de.value_domain_id
                domain_name = domain.name if domain else "Unknown"
                lines.append(f'  {de.name} : {domain_name}')

            # Constraint をメソッドとして出力
            oc_constraints = Constraints.filtered(lambda c: c.object_class_id.id == oc.id)
            for c in oc_constraints:
                targets = ConstraintTargets.filtered(lambda t: t.constraint_id.id == c.id)
                args = [t.data_element_id.name for t in targets if t.data_element_id]
                args_text = ", ".join(args)
                lines.append(f'  - {c.name}({args_text})')

            lines.append("}")

        # ---------------------------------------------------------
        # relation / extended のリンク
        # ---------------------------------------------------------
        for de in DataElements:
            src_oc = de.object_class_id
            src_name = f"{src_oc.system_id.name}.{src_oc.name}" if src_oc.system_id else src_oc.name

            vd = de.value_domain_id
            if not vd:
                continue

            # relation
            if vd.data_type == "relation" and vd.relation_object_class_id:
                tgt_oc = vd.relation_object_class_id
                tgt_name = f"{tgt_oc.system_id.name}.{tgt_oc.name}" if tgt_oc.system_id else tgt_oc.name
                lines.append(f'"{tgt_name}" --{{ "{src_name}" : "{de.name}"')

            # extended
            if vd.data_type == "extended" and vd.relation_object_class_id:
                tgt_oc = vd.relation_object_class_id
                tgt_name = f"{tgt_oc.system_id.name}.{tgt_oc.name}" if tgt_oc.system_id else tgt_oc.name
                lines.append(f'"{tgt_name}" <|-- "{src_name}"')

        # ---------------------------------------------------------
        # ConstraintTarget のリンク
        # ---------------------------------------------------------
        for t in ConstraintTargets:
            c = t.constraint_id
            de = t.data_element_id
            if not c or not de:
                continue

            src_oc = c.object_class_id
            tgt_oc = de.object_class_id

            src_name = f"{src_oc.system_id.name}.{src_oc.name}" if src_oc.system_id else src_oc.name
            tgt_name = f"{tgt_oc.system_id.name}.{tgt_oc.name}" if tgt_oc.system_id else tgt_oc.name

            lines.append(f'"{src_name}" .. "{tgt_name}" : "{c.name}"')

        # ---------------------------------------------------------
        # ★ Constraint.description を note として出力
        # ---------------------------------------------------------
        generate_note = self.env.context.get('generate_note', True)
        if generate_note:
            note_counter = 0

            for c in Constraints:
                if not c.description:
                    continue

                note_counter += 1
                note_name = f"note{note_counter:03d}"

                # 改行を PlantUML 用に変換
                note_body = f"{c.name}\n{c.description}".replace("\n", "\\n")

                # note 出力
                lines.append(f'note "{note_body}" as {note_name}')

                # note のリンク先（Constraint の ObjectClass）
                oc = c.object_class_id
                entity_name = f"{oc.system_id.name}.{oc.name}" if oc.system_id else oc.name

                lines.append(f'{entity_name} .. "{note_name}" : "{c.name}"')

        lines.append("@enduml")
        return lines

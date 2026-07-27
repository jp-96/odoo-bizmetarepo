from odoo import models
from .uml_base import BaseUmlGenerator

class LdmUmlGenerator(BaseUmlGenerator):
    _name = "ems.uml.ldm_generator"
    _description = "LDM UML Generator"

    def build_uml_lines(self):
        ObjectClasses = self.env["ems.ldm.object_class"].search([])
        DataElements = self.env["ems.ldm.data_element"].search([])

        lines = []
        lines.append("@startuml")

        for oc in ObjectClasses:
            prefix = oc.system_id.name if oc.system_id else ""
            entity_name = f"{prefix}.{oc.name}" if prefix else oc.name

            lines.append(f'entity "{entity_name}" {{')

            oc_elements = DataElements.filtered(lambda d: d.object_class_id.id == oc.id)
            for de in oc_elements:
                domain_name = de.value_domain_id.name if de.value_domain_id else "Unknown"
                lines.append(f'  {de.name} : {domain_name}')

            lines.append("}")

        lines.append("@enduml")
        return lines

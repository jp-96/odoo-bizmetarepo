from odoo import models, fields, api
import zlib
import base64
import requests
import logging
_logger = logging.getLogger(__name__)

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
    zlibbed = zlib.compress(text.encode("utf-8"))
    data = zlibbed[2:-4]
    res = []
    for i in range(0, len(data), 3):
        b1 = data[i]
        b2 = data[i + 1] if i + 1 < len(data) else 0
        b3 = data[i + 2] if i + 2 < len(data) else 0
        res.append(_append_3bytes(b1, b2, b3))
    return "".join(res)


class UmlGenerator(models.TransientModel):
    _name = "ems.ldm.uml_generator"
    _description = "ems.ldm UML Generator"

    uml_text = fields.Text(string="UML（編集可能）")
    uml_png_url = fields.Char(string="PNG URL")
    uml_png = fields.Binary(string="UML PNG")

    def generate_uml(self):
        ObjectClasses = self.env["ems.ldm.object_class"].search([])
        DataElements = self.env["ems.ldm.data_element"].search([])
        ValueDomains = self.env["ems.ldm.value_domain"].search([])

        lines = []
        lines.append("@startuml")

        # ---------------------------------------------------------
        # ObjectClass → entity
        # ---------------------------------------------------------
        for oc in ObjectClasses:
            prefix = oc.system_id.name if oc.system_id else ""
            entity_name = f"{prefix}.{oc.name}" if prefix else oc.name

            lines.append(f'entity "{entity_name}" {{')

            # ---------------------------------------------------------
            # DataElement → 属性
            # ---------------------------------------------------------
            oc_elements = DataElements.filtered(lambda d: d.object_class_id.id == oc.id)

            for de in oc_elements:
                domain = de.value_domain_id
                domain_name = domain.name if domain else "Unknown"
                lines.append(f'  {de.name} : {domain_name}')

            lines.append("}")

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
            "res_model": "ems.ldm.uml_generator",
            "view_mode": "form",
            "target": "new",
            "res_id": self.id,
        }

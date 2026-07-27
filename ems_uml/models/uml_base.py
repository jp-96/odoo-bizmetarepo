from odoo import models, fields
import zlib
import base64
import requests
import logging

_logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# PlantUML エンコード（共通）
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# 抽象基底クラス
# ---------------------------------------------------------
class BaseUmlGenerator(models.TransientModel):
    # _name = "ems.uml.base_generator"
    _description = "Base UML Generator"
    # _abstract = True

    uml_text = fields.Text(string="UML（編集可能）")
    uml_png_url = fields.Char(string="PNG URL")
    uml_png = fields.Binary(string="UML PNG")

    # ---------------------------------------------------------
    # サブクラスが実装するメソッド
    # ---------------------------------------------------------
    def build_uml_lines(self):
        raise NotImplementedError("Subclasses must implement build_uml_lines()")

    # ---------------------------------------------------------
    # 共通 UML 生成処理
    # ---------------------------------------------------------
    def generate_uml(self):
        lines = self.build_uml_lines()
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
            "res_model": self._name,
            "view_mode": "form",
            "target": "new",
            "res_id": self.id,
        }

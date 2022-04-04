from odoo import fields,models,api
from datetime import datetime
import convert_numbers
from uuid import uuid4
import qrcode
import base64
import logging
from lxml import etree
import werkzeug.urls
try:
    import qrcode
except ImportError:
    qrcode = None

class ProFormaInvoice(models.Model):
    _inherit = 'pro.forma.invoice'


    currency_id = fields.Many2one('res.currency',default=lambda self: self.env.company.currency_id.id,readonly=0,related=None)


    @api.depends('invoice_line_ids','advance_amount')
    def compute_tax(self):
        for invoice in self:
            percentage = 0
            for line in invoice.invoice_line_ids:
                for line_tax in line.tax_ids:
                    percentage = line_tax.amount
            invoice.amount_tax = '{:.2f}'.format((invoice.advance_amount / 100) * percentage)


    def ar_total_tax(self):
        value = self.amount_untaxed * 0.15
        before, after = str('{:.2f}'.format(value)).split('.')
        before_int = int(before)
        after_int =after
        before_ar = convert_numbers.english_to_arabic(before_int)
        after_ar = convert_numbers.english_to_arabic(after_int)
        ar_total_tax_amount = before_ar + '.' + after_ar
        return before_ar + '.' + after_ar
    def ar_discount_value(self):
        value = self.discount
        before, after = str(value).split('.')
        before_int = int(before)
        after_int = int(after)
        before_ar = convert_numbers.english_to_arabic(before_int)
        after_ar = convert_numbers.english_to_arabic(after_int)
        # ar_total_tax_amount = before_ar + '.' + after_ar + ' ' + self.currency_id.name
        ar_total_tax_amount = before_ar + '.' + after_ar + ' ' + self.currency_id.name
        # return before_ar + '.' + after_ar + ' '+ self.currency_id.name
        return before_ar + '.' + after_ar

    def testing(self):
        leng = len(self.company_id.name)
        company_name = self.company_id.name
        if 42 > leng:
            for r in range(42-leng):
                if len(company_name) != 42:
                   company_name +=' '
                else:
                    break
        else:
            if 42 < leng:
                company_name = company_name[:42]
        vat_leng = len(self.company_id.vat)
        vat_name = self.company_id.vat
        if 17 > vat_leng:
            for r in range(15 - vat_leng):
                if len(vat_name) != 15:
                    vat_name += ' '
                else:
                    break
        else:
            if 17 < leng:
                vat_name = vat_name[:17]
        amount_total = str(self.amount_total / self.currency_id.rate)
        amount_leng = len(str(self.amount_total / self.currency_id.rate))
        if len(amount_total) < 17:
            for r in range(17-amount_leng):
                if len(amount_total) != 17:
                   amount_total +=' '
                else:
                    break

        tax_leng = len(str(self.amount_tax / self.currency_id.rate))
        amount_tax_total = str(self.amount_tax / self.currency_id.rate)
        if len(amount_tax_total) < 17:
            for r in range(17-tax_leng):
                if len(amount_tax_total) != 17:
                   amount_tax_total +=' '
                else:
                    break
        TimeAndDate = str(self.invoice_date_time) + "T" + str(self.datetime_field.time()) + "Z"
        time_length = len(str(self.invoice_date_time) + "T" + str(self.datetime_field.time()) + "Z")

        Data = str(chr(1)) + str(chr(leng)) + self.company_id.name
        Data += (str(chr(2))) + (str(chr(vat_leng))) + vat_name
        Data += (str(chr(3))) + (str(chr(time_length))) + TimeAndDate
        # Data += (str(chr(4))) + (str(chr(len(str(self.amount_total / self.currency_id.rate))))) + str(self.amount_total / self.currency_id.rate)
        Data += (str(chr(4))) + (str(chr(len(str(self.amount_total * self.currency_id.rate)))))+ str(self.amount_total * self.currency_id.rate)
        # Data += (str(chr(5))) + (str(chr(len(str(self.amount_tax / self.currency_id.rate))))) + str(self.amount_tax / self.currency_id.rate)
        Data += (str(chr(5))) + (str(chr(len(str(self.amount_tax * self.currency_id.rate)))))+ str(self.amount_tax * self.currency_id.rate)
        data = Data
        import base64
        mou = base64.b64encode(bytes(data, 'utf-8'))
        self.decoded_data = str(mou.decode())
        qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=20,
                border=4,
            )
        data_im = str(mou.decode())
        qr.add_data(data_im)
        qr.make(fit=True)
        img = qr.make_image()

        import io
        import base64

        temp = io.BytesIO()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        self.qr_image = qr_image
        return str(mou.decode())
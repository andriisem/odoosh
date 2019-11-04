from ..shipstation_api import (
    ShipStationBase,
    ShipStationCustomsItem,
    ShipStationInternationalOptions,
    ShipStationWeight,
    ShipStationContainer,
    ShipStationItem,
    ShipStationAddress,
    ShipStationOrder,
    ShipStation)
    
from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_process_shipment(self):
        ship_station_address = ShipStationAddress(
            name=self.partner_id.name,
            company=self.partner_id.name,
            street1=self.partner_id.street,
            street2=self.partner_id.street2,
            city=self.partner_id.city,
            state=self.partner_id.state_id.name,
            postal_code=self.partner_id.zip,
            country=self.partner_id.country_id.name,
            phone=self.partner_id.phone,
        )

        ship_station_order = ShipStationOrder(
            order_number=self.name
        )
        
        # DIMENSIONS
        # ship_station_container = ShipStationContainer()
        
        # ship_station_container.set_weight(weight)
        # ship_station_order.set_dimensions(ship_station_container)
        
        # STATUS
        ship_station_order.set_status('awaiting_payment')
        ship_station_order.set_shipping_address(ship_station_address)
        ship_station_order.set_billing_address(ship_station_address)

        for line in self.order_line:
            item = ShipStationItem(
                sku=line.product_id.barcode,
                name=line.name,
                quantity=int(line.product_uom_qty),
                unit_price=line.price_unit,
            )
            weight = ShipStationWeight(units='ounces', value=line.product_id.weight)
            item.set_weight(weight)
            ship_station_order.add_item(item)
        
        for api_conf in self.env['ship.station.config'].search([]):
            ss = ShipStation(key=api_conf.api_key, secret=api_conf.api_secret_key, debug=True)
            ss.add_order(ship_station_order)
            ss.submit_orders()

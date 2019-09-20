FROM andriisem/custom:odoo-12.0ee-20191009-dubug
USER root
RUN pip3 install future
USER odoo
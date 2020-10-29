Using this documentation 
https://hub.docker.com/_/odoo
https://www.odoo.com/documentation/14.0/howtos/backend.html
https://www.odoo.com/documentation/14.0/reference/orm.html


do this steps: 
1. Make the field "internal_ref" readonly.
2. Under internal reference add a relational field Many2one on to select a user.
3. Add an "on change" hook to update the internal ref with the 'Hello <username>'

![END GAME](https://github.com/blackware-technologies/odoo-technical-test/blob/master/img/endgame.PNG?raw=true)


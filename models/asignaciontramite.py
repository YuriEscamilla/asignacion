
from odoo import models,fields, api
from odoo.exceptions import UserError

class asignaciontramite(models.Model):
    _name = 'asignacion.tramite.gestion'
    _rec_name = 'RefIdGestion'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    RefIdGestion = fields.Many2one(comodel_name='tramite.gestion',
                                   string='Folio de la Solicitud')
    RefIdIAP = fields.Many2one(related="RefIdGestion.RefIdIAP")
    RefIdTipoTram = fields.Many2one(related="RefIdGestion.RefIdTipoTram")
    RefidSolicitud = fields.Integer(related="RefIdGestion.RefidSolicitud")
    RefIdUsuario = fields.Many2one(related="RefIdGestion.RefIdUsuario")
    origeningreso = fields.Selection(related="RefIdGestion.origeningreso")


    RefIdUserAnterior = fields.Many2one(comodel_name='res.users')
    RefIdUserActual = fields.Many2one(comodel_name='res.users', domain=[('login', 'like', '@jap.cdmx.gob.mx')])

    documento_direccion = fields.Selection([('no','NO'),('si','SI')], default='si', string="¿La solicitud pertenece a la Dirección?")
    documento_anexa = fields.Selection([('no', 'NO'), ('si', 'SI')], default='si',
                                           string="¿La solicitud anexa pertenece a la solicitud ingresada?")


    refid_tramanterior = fields.Many2one(comodel_name='cf.tipos.tramites')
    refid_tramactual = fields.Many2one(comodel_name='cf.tipos.tramites', domain="[('id','not in',('1','2','3','9','17','33','34'))]")




            

    def asignar_asesor(self):

        for record in self:
            filtros_gestion = [('id','=',self.RefIdGestion.id),('RefidSolicitud','=',self.RefidSolicitud)]
            tipo_tramite_asignar = self.env['tramite.gestion'].sudo().search(filtros_gestion)


            self.RefIdUserAnterior = tipo_tramite_asignar.RefIdUsuario.id
            self.refid_tramanterior = tipo_tramite_asignar.RefIdTipoTram.id

            print(self.RefIdUserAnterior)
            print(self.RefIdUserActual)

            #SI EL ORIGEN DE INGRESO ES POR MODULO DE SOLICITUD
            if tipo_tramite_asignar.origeningreso == "1":
                #SI EL TIPO DE TRAMITE ES ESTADOS FINANCIEROS
                if tipo_tramite_asignar.RefIdTipoTram.id == 1:

                    filtro = [('RefidSolicitud','=',self.RefidSolicitud)]
                    gestion_tramite = self.env['tramite.gestion.estadosfin'].sudo().search(filtro)



                #SI EL TIPO DE TRAMITE ES CONTRATOS DE ARRENDAMIENTO
                elif tipo_tramite_asignar.RefIdTipoTram.id == 2:
                    filtro = [('RefidSolicitud', '=', self.RefidSolicitud)]
                    gestion_tramite = self.env['tramite.gestion.sicoarre'].sudo().search(filtro)


                #SI EL TIPO DE TRAMITE ES JUICIOS
                elif tipo_tramite_asignar.RefIdTipoTram.id == 3:
                    filtro = [('RefidSolicitud', '=', self.RefidSolicitud)]
                    gestion_tramite = self.env['tramite.gestion.juicios'].sudo().search(filtro)

                # Si el tipo de tramite ENAJENACION DE BIENES MUEBLES
                elif tipo_tramite_asignar.RefIdTipoTram.id == 16:
                    filtro = [('RefidSolicitud', '=', self.RefidSolicitud)]
                    gestion_tramite = self.env['tramite.gestion.enajenacion'].sudo().search(filtro)

                # Si el tipo de tramite ENAJENACION DE BIENES INMUEBLES
                elif tipo_tramite_asignar.RefIdTipoTram.id == 13:
                    filtro = [('RefidSolicitud', '=', self.RefidSolicitud)]
                    gestion_tramite = self.env['tramite.gestion.enajenacion'].sudo().search(filtro)

                # Si el tipo de tramite ENAJENACION DE BIENES GRAVAMEN
                elif tipo_tramite_asignar.RefIdTipoTram.id == 14:
                    filtro = [('RefidSolicitud', '=', self.RefidSolicitud)]
                    gestion_tramite = self.env['tramite.gestion.gravamen'].sudo().search(filtro)

                actualiza_asesor_tramite = {'RefIdUsuario': record.RefIdUserActual.id}
                gestion_tramite.sudo().write(actualiza_asesor_tramite)

                actualiza_asesor = {'RefIdUsuario': self.RefIdUserActual.id}
                tipo_tramite_asignar.sudo().write(actualiza_asesor)

            elif tipo_tramite_asignar.origeningreso == "2":
                filtrosop = [('refidAtencion', '=', self.RefidSolicitud)]
                etapa_gestion_tram = self.env['responder.atencion.virtual'].sudo().search(filtrosop)

                #actualiza la tabla de responder_atencion para la gestion del tramite
                actualiza_asesor_tramite = {'userasignado': record.RefIdUserActual.id}
                etapa_gestion_tram.sudo().write(actualiza_asesor_tramite)

                #actualiza la tabla tramite_Gestion para la consulta general
                actualiza_asesor = {'RefIdUsuario': self.RefIdUserActual.id}
                tipo_tramite_asignar.sudo().write(actualiza_asesor)

                if self.documento_direccion == 'si' and self.documento_anexa == 'no':

                    if self.refid_tramactual == False:
                        raise UserError('Es necesario seleccionar un tipo de trámite')

                    folio_atencion_virtual = self.env['atencion.virtual'].sudo().search([('id','=',self.RefidSolicitud)])

                    #actualiza la tabla de atencion virtual y cambiar el tipo de tramite
                    actualiza_tipo_tramite = {'tipotram': self.refid_tramactual}
                    folio_atencion_virtual.sudo().write(actualiza_tipo_tramite)

                    #actualia la tabla de tramite gestion y cambiar el tipo de tramite
                    actualiza_tipo_tramite = {'RefIdTipoTram': self.refid_tramactual}
                    tipo_tramite_asignar.sudo().write(actualiza_tipo_tramite)


            template = self.env.ref('asignacion.asignacion_folio')
            template.send_mail(self.id, force_send=True)

            '''if self.documento_direccion == 'si' and self.documento_anexa == 'no':

                if self.refid_tramactual == False:
                    raise UserError('Es necesario seleccionar un tipo de trámite')
                actualiza_asesor = {'RefIdUsuario': self.RefIdUserActual.id,
                                    'RefIdTipoTram': self.refid_tramactual}

            else:



                actualiza_asesor = {'RefIdUsuario': self.RefIdUserActual.id}
                tipo_tramite_asignar.sudo().write(actualiza_asesor)
'''








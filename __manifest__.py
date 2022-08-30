{
    'name': 'ASIGNACION DE TRAMITES',
    'version': '1.0',
    'category': 'Modulo de JAP',
    'sequence': 15,
    'author':'DTIC - JAPDF',
    'summary': 'ASIGNACION DE TRAMITES',
    'description': 'MODULO QUE LLEVA A CABO LA ASIGNACION DE TRAMITES',


    'depends': ['base','mail','gestiontramites'],

    'data': [


        'views/asignacion_tramite_view.xml',
        'views/asignacion_tramites_ingresados_view.xml',
        'security/tools_jap_security.xml',
        'security/ir.model.access.csv',
        'datas/template_mail_view.xml',
        'views/asignacion_menu_tramite_view.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
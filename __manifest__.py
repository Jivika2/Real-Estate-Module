{
    "name" : "Real Estate Ads",
    "version" : "1.0",
    "website" : "https//www.jivika.com",
    "author" : "jivika",
    "description" : """
        Real Estate module to show available properties
        """,
    "category" : "Sales",
    "depends" : ['web','mail','utm','website'],
    "data" : [
        'security/ir.model.access.csv',
        'security/model_access.xml',
        'security/ir_rule.xml',
        'security/res_groups.xml',
        'views/property_view.xml',
        'views/property_type.xml',
        'views/property_tag.xml',
        'views/property_offer_view.xml',
        'views/menuitems.xml',

        #'data/property_type.xml',
        'data/estate.property.type.csv',
        'data/mail_template.xml',
        'report/report_template.xml',
        'report/property_report.xml',
        
    ],

    'demo': [
        'demo/property_tag.xml'
    ],

    'assets': {
        'web.assets_backend': [
            'real_estate_ads/static/src/js/my_custom_tag.js',
            'real_estate_ads/static/src/xml/my_custom_tags.xml',
        ]
    },
    "installable" : True,
    "application" : True,
    "license" : "LGPL-3"
}
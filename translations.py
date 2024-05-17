translations = { 
'en': {
        'Tu enlace de invitación:': 'Your invitation link:',
        'Ir a nuestro grupo': 'Go to our group',
        'No puedes usar tu enlace de referencia': 'You cannot use your referral link',
        '📑 Estadísticas': '📑 Statistics',
        '🇪🇸 Cambiar de idioma': '🇬🇧 Change language',
        'Invitaste a': 'You invited',
        'No puede utilizar su enlace de referencia': 'You cannot use your referral link',
        'Invita a gente al grupo y consigue un premio': 'Invite people to the group and get a prize',
        'Hola': 'Hi',
        'Tu rango': 'Your rank',
        'Actualizar': 'Refresh',
        'Volver al menú': 'Back to menu',
        'Los 10 primeros usuarios por número de invitaciones al grupo': 'Top 10 users by number of invitations to the group'
    }
}

def _(text, lang='sp'):
    if lang == 'sp':
        return text
    else:
        global translations
        try:
            return translations[lang][text]
        except:
            return text
        
import csv
import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    Base,
    PlayerRoles,
    Teams,
    Player,
    Statistics
    )

ROLES = {'goalkeeper' : 'Goalkeeper',
         'defender'   : 'Defender',
         'midfielder' : 'Midfielder',
         'striker'    : 'Striker'}

TEAMS = {'Ata.': u'Atalanta',
         'Bol.': u'Bologna',
         'Cag.': u'Cagliari',
         'Cat.': u'Catania',
         'Chi.': u'Chievo',
         'Fio.': u'Fiorentina',
         'Gen.': u'Genoa',
         'Int.': u'Inter',
         'Juv.': u'Juventus',
         'Laz.': u'Lazio',
         'Liv.': u'Livorno',
         'Mil.': u'Milan',
         'Nap.': u'Napoli',
         'Par.': u'Parma',
         'Rom.': u'Roma',
         'Sam.': u'Sampdoria',
         'Sas.': u'Sassuolo',
         'Tor.': u'Torino',
         'Udi.': u'Udinese',
         'Ver.': u'Verona'
     }


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n arg'
          '(example: "%s development.ini" roles)' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 3:
        usage(argv)
    config_uri = argv[1]
    which = argv[2]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        if which == 'roles':
            for role in ROLES:
                model = PlayerRoles(name=role, label=ROLES[role])
                DBSession.add(model)
        elif which == 'teams':
            for shortname in TEAMS:
                model = Teams(shortname=shortname, fullname=TEAMS[shortname])
                DBSession.add(model)
        elif which == 'players':
            ## get teams like
            ## id | shortname |  fullname  
            ## ----+-----------+------------
            ##   1 | Gen.      | Genoa
            ##   2 | Tor.      | Torino
            ##   3 | Sas.      | Sassuolo
            teams = DBSession.query(Teams).all()
            team_code = {}
            for team in teams:
                team_code[team.fullname.upper()] = team.id

            ##roles are
            ## id |    name    |   label    
            ##----+------------+------------
            ##  1 | defender   | Defender
            ##  2 | striker    | Striker
            ##  3 | goalkeeper | Goalkeeper
            ##  4 | midfielder | Midfielder
            role_code = {'P': 3,
                         'D': 1,
                         'C': 4,
                         'A': 2}
            with open('statistiche.csv', 'rb') as csvfile:
                rows = csv.reader(csvfile, delimiter=';')
                rows.next() #skip header
                counter = 0
                for row in rows:
                    player = Player(role_code[row[1]], team_code[row[3]],
                                    u'', row[2].lower().capitalize().decode('utf-8'),
                                    True)
                    DBSession.add(player)
        else:
            teams = DBSession.query(Teams).all()
            team_code = {}
            for team in teams:
                team_code[team.fullname.upper()] = team.id

            ##roles are
            ## id |    name    |   label    
            ##----+------------+------------
            ##  1 | defender   | Defender
            ##  2 | striker    | Striker
            ##  3 | goalkeeper | Goalkeeper
            ##  4 | midfielder | Midfielder
            role_code = {'P': 3,
                         'D': 1,
                         'C': 4,
                         'A': 2}
            import pdb;pdb.set_trace()
            with open('statistiche.csv', 'rb') as csvfile:
                rows = csv.reader(csvfile, delimiter=';')
                rows.next() #skip header
                counter = 1
                for row in rows:
                    statistics = Statistics('2012/2013', counter,
                                            int(row[4]), float(row[16].replace(',', '.')),
                                            int(row[9]), int(row[13]),
                                            int(row[7]), int(row[8]),
                                            int(row[10]), int(row[12]),
                                            int(row[11]), int(row[5]),
                                            int(row[6])
                                           )
                    DBSession.add(statistics)
                    counter += 1

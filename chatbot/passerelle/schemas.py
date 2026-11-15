"""Liste blanche des requêtes autorisées sur le modèle, et validation stricte de leurs arguments.

Source unique : la passerelle valide chaque requête contre ces schémas AVANT d'appeler le modèle, et le chatbot
les récupère (GET /v1/outils) pour les déclarer au modèle de langage. Aucune requête hors de cette liste n'existe.
Pas de bibliothèque externe : le sous-ensemble de JSON Schema utilisé est vérifié ici, et tout le reste est refusé.
"""
from __future__ import annotations

MAX_TEXTE = 500
MAX_LISTE = 10

_LV = {
    "quotas": {"type": "number", "minimum": 0.7, "maximum": 1.5, "description": "Places en formation, multiplicateur (1.2 = +20 %). Effet après la durée des études."},
    "quotas_region": {"type": "boolean", "description": "Hausse des places seulement dans la région du territoire demandé."},
    "etrangers": {"type": "number", "minimum": 0, "maximum": 2.0, "description": "Diplômés hors de France accueillis, multiplicateur."},
    "regul": {"type": "boolean", "description": "Régulation de l'installation : en zone régulée, une entrée seulement pour un départ."},
    "part_zones": {"type": "number", "minimum": 0.0, "maximum": 1.0, "description": "Part des zones régulées retenues, si regul."},
    "dest": {"type": "string", "enum": ["salariat", "sortie", "voisine"], "description": "Destination des entrants bloqués, si regul."},
    "retraite": {"type": "number", "minimum": 0.0, "maximum": 3.0, "description": "Report de la cessation d'activité, en années (pas 0.5)."},
    "cumul": {"type": "number", "minimum": 0.5, "maximum": 2.0, "description": "Cumul emploi-retraite, multiplicateur."},
    "precoces": {"type": "number", "minimum": 0.5, "maximum": 1.5, "description": "Départs avant 60 ans, multiplicateur (0.5 = moitié moins)."},
    "pop_scen": {"type": "string", "enum": ["central", "pop_basse", "pop_haute"], "description": "Scénario de population Insee Omphale 2022 (densités)."},
    "activite": {"type": "number", "minimum": 0.8, "maximum": 1.1, "description": "Activité moyenne par professionnel, hypothèse supposée (densités)."},
}
LEVIERS = {"type": "object", "properties": _LV, "additionalProperties": False,
           "description": "Seulement les leviers modifiés ; les autres restent au tendanciel."}
PROF = {"type": "string", "enum": ["sages-femmes", "dentistes", "pharmaciens", "kines", "infirmiers"]}
TERR = {"type": "string", "maxLength": 80,
        "description": "« France », une région, un département (nom ou numéro) ou une ville ; codes FR, R84, D63 acceptés."}
ANNEE = {"type": "integer", "minimum": 2026, "maximum": 2050}
SCALAIRE = {"anyOf": [{"type": "number"}, {"type": "boolean"}, {"type": "string", "maxLength": 20}]}


def _obj(props: dict, req: list) -> dict:
    return {"type": "object", "properties": props, "required": req, "additionalProperties": False}


# Transfert de tâches hypothétique (forme de L23) : bornes de GET /api/couverture (tr_*) de la carte
TRANSFERT = _obj({"source": {"type": "string", "enum": ["medecine-generale", "specialistes", *PROF["enum"]]},
                  "cible": PROF,
                  "a": {"type": "number", "minimum": 0, "maximum": 0.5, "description": "Part de la demande de la source concernée par l'acte (poids de l'acte). Ne pas la déduire de « p % des <acte> » : laisser vide, la passerelle balaie 5, 10 et 20 %."},
                  "s_inf": {"type": "number", "minimum": 0, "maximum": 1, "description": "Part de l'acte transférée à terme : « p % des <acte> » donne s_inf = p/100."},
                  "k": {"type": "number", "minimum": 0.1, "maximum": 3, "description": "Temps de la cible par unité de temps de la source."},
                  "tau": {"type": "number", "minimum": 0.1, "maximum": 20, "description": "Montée en charge, années."},
                  "t0": {"type": "integer", "minimum": 2026, "maximum": 2050, "description": "Année d'autorisation."}},
                 ["source", "cible"])


# nom -> (description pour le modèle de langage, schéma des arguments)
OUTILS: dict[str, tuple[str, dict]] = {
    "perimetre": ("Ce que le modèle couvre et ne couvre PAS (professions, grain, années, sujets hors périmètre, politiques non "
                  "modélisées avec leur raison). À appeler dès qu'une question pourrait sortir du périmètre.", _obj({}, [])),
    "projeter": ("Projette l'effectif libéral d'une profession sur un territoire : tendanciel et scénario aux années demandées, "
                 "fourchette, densité pour 100 000 habitants, écart par flux, provenance des leviers.",
                 _obj({"profession": PROF, "territoire": TERR, "leviers": LEVIERS,
                       "annees": {"type": "array", "items": ANNEE, "maxItems": MAX_LISTE, "description": "Défaut : 2030, 2035, 2040, 2050."}},
                      ["profession"])),
    "comparer": ("Compare de 1 à 6 scénarios (réglages de leviers) pour une profession et un territoire, à une année.",
                 _obj({"profession": PROF, "territoire": TERR, "annee": ANNEE,
                       "scenarios": {"type": "array", "maxItems": 6,
                                     "items": _obj({"nom": {"type": "string", "maxLength": 80}, "leviers": LEVIERS}, ["leviers"])}},
                      ["profession", "territoire", "scenarios"])),
    "balayer": ("Sensibilité d'UN levier : effectif à une année pour plusieurs valeurs de ce levier, les autres fixés.",
                _obj({"profession": PROF, "territoire": TERR, "levier": {"type": "string", "enum": list(_LV)},
                      "valeurs": {"type": "array", "items": SCALAIRE, "maxItems": 9}, "annee": ANNEE, "autres_leviers": LEVIERS},
                     ["profession", "territoire", "levier", "valeurs"])),
    "classer": ("Classe les départements d'une région (ou de France) par densité, écart au tendanciel ou évolution.",
                _obj({"profession": PROF, "region": {"type": "string", "maxLength": 80, "description": "Vide = France."},
                      "leviers": LEVIERS, "annee": ANNEE,
                      "critere": {"type": "string", "enum": ["densite_100k_scenario", "ecart_pct", "evolution_pct_depuis_origine", "scenario"]},
                      "ordre": {"type": "string", "enum": ["croissant", "decroissant"]},
                      "n": {"type": "integer", "minimum": 1, "maximum": 30}},
                     ["profession"])),
    "atteindre": ("Problème inverse : pour atteindre un objectif (+X % de densité ou d'effectif en une année, par rapport au "
                  "tendanciel ou à aujourd'hui), quel réglage de chaque levier faut-il, seul ? Et tous au maximum, est-ce atteint ? "
                  "À utiliser pour « comment atteindre / que faudrait-il pour / objectif de ».",
                  _obj({"profession": PROF, "territoire": TERR, "hausse_pct": {"type": "number", "minimum": 0.5, "maximum": 200},
                        "annee": ANNEE, "grandeur": {"type": "string", "enum": ["densite", "effectif"]},
                        "reference": {"type": "string", "enum": ["tendanciel", "origine"],
                                      "description": "tendanciel : même année sans politique (défaut) ; origine : aujourd'hui."}},
                       ["profession", "territoire", "hausse_pct"])),
    "traduire_politique": ("POLITIQUE HORS MODÈLE -> leviers du même mécanisme. Pour une politique de la liste « politiques_non_modelisees » "
                           "du périmètre (aides à l'installation, rémunération, maisons de santé, obligation en zone, CESP…), renvoie "
                           "la traduction SUPPOSÉE (leviers, sens, mécanisme, limite) et deux essais (ampleur basse et haute), ou « pas "
                           "dans le modèle » s'il n'y a aucun mécanisme commun.",
                           _obj({"politique": {"type": "string", "enum": ["obligation_zone", "exercice_coordonne", "remuneration",
                                 "duree_etudes", "aides_installation", "cesp", "vaccination_officine", "ipa", "acces_direct", "tension_diabete",
                                 "teleconsultation", "quatrieme_annee_mg", "medecins_specialistes"]},
                                 "profession": PROF, "territoire": TERR, "annee": ANNEE}, ["politique", "profession"])),
    "planifier": ("OBJECTIF -> LEVIERS. Pour une cible chiffrée à un horizon (« je veux +X % », « atteindre N pour 100 000 », "
                  "« quels leviers actionner pour… », « doubler… »), renvoie : les deux lectures (par rapport à aujourd'hui et à la "
                  "tendance), si la tendance l'atteint déjà, et sinon 1 à 3 mélanges de leviers vérifiés par le jumeau (le plus simple, "
                  "le plus tôt, prudent), avec délai, premier effet, année limite de décision, statut et fourchette.",
                  _obj({"profession": PROF, "territoire": TERR, "annee": ANNEE,
                        "grandeur": {"type": "string", "enum": ["effectif", "densite"]},
                        "hausse_pct": {"type": "number", "minimum": 0.5, "maximum": 300},
                        "valeur_cible": {"type": "number", "minimum": 0, "maximum": 1000000,
                                         "description": "cible absolue (effectif, ou densité pour 100 000 si grandeur = densite)"},
                        "reference": {"type": "string", "enum": ["tendanciel", "origine"]},
                        "leviers_exclus": {"type": "array", "maxItems": 5, "items": {"type": "string", "enum": ["quotas", "etrangers", "retraite", "cumul", "precoces"]}},
                        "n_max_leviers": {"type": "integer", "minimum": 1, "maximum": 5}},
                       ["profession"])),
    "effets_des_leviers": ("Compare l'effet de CHAQUE levier seul, à un réglage de référence, puis de tous ensemble, pour une "
                           "profession, un territoire et une année. À utiliser pour « quelles politiques ont le plus d'effet », "
                           "« quoi d'autre », « par quoi commencer ».",
                           _obj({"profession": PROF, "territoire": TERR, "annee": ANNEE}, ["profession"])),
    "couverture": ("INDICE DE COUVERTURE (module de besoin) d'une des cinq professions : offre / demande de soins de ville, base 2026 = 1, tendanciel "
                   "et scénario, écart relatif au tendanciel, fourchette entre estimateurs si le choix du modèle pèse. Levier L23 "
                   "(vaccination en officine, à partir de l23_t0) : l'effectif ne change pas, la couverture des pharmaciens oui. "
                   "Jamais pour la médecine générale ni les spécialistes (règle O2). Transfert HYPOTHÉTIQUE (`transfert`) : une part "
                   "a de la demande de la source (MG, spécialistes ou l'une des cinq) passe vers la cible (l'une des cinq), forme "
                   "de L23 ; paramètres de l'utilisateur·rice, jamais un levier sourcé. « p % DES <acte> » : s_inf = p/100, a non "
                   "donné ; « p % DE LA DEMANDE » : a = p/100. Le résultat donne `balayage_a` (3 valeurs de a) : les citer toutes.",
                   _obj({"profession": PROF, "territoire": TERR, "leviers": LEVIERS, "transfert": TRANSFERT,
                         "l23": {"type": "boolean", "description": "Vaccination en officine (transfert L23) active ; défaut : non. Seulement si la question parle de vaccination."},
                         "l23_t0": {"type": "integer", "minimum": 2019, "maximum": 2050, "description": "Année d'autorisation (défaut 2026)."},
                         "effectivite": {"type": "boolean", "description": "Avec l23 et les pharmaciens : le transfert soulage-t-il la médecine générale sans trop peser sur les pharmaciens ? Couverture de la source et de la cible avec et sans transfert, plage de k, verdict (décision O3). Seulement si la question le demande."},
                         "offre_mg": {"type": "string", "enum": ["constante", "nationale", "externe"], "description": "Offre de médecine générale lue en entrée pour l'effectivité ; défaut constante (RPPS 2026, supposé)."},
                         "annees": {"type": "array", "items": ANNEE, "maxItems": MAX_LISTE}}, ["profession"])),
    "decrire_leviers": ("Leviers du modèle : bornes, délai d'effet, statut (sourcé / supposé), source.", _obj({}, [])),
    "incertitude": ("Indices de Sobol (axe 5) : quels paramètres et choix d'estimation pèsent le plus sur la projection.",
                    _obj({"profession": PROF, "annee": {"type": "integer", "enum": [2030, 2040, 2050]}}, ["profession"])),
    "interpreter_phrase": ("Compilateur déterministe de l'équipe (glossaire) : traduction d'une phrase en leviers et politiques "
                           "non modélisées détectées. Pour vérifier une interprétation.",
                           _obj({"texte": {"type": "string", "maxLength": MAX_TEXTE}}, ["texte"])),
}


class Invalide(ValueError):
    pass


def valider(schema: dict, x, chemin: str = "arguments") -> None:
    """Vérifie x contre le sous-ensemble de JSON Schema ci-dessus ; lève Invalide au premier écart."""
    if "anyOf" in schema:
        for s in schema["anyOf"]:
            try:
                return valider(s, x, chemin)
            except Invalide:
                pass
        raise Invalide(f"{chemin} : type non accepté")
    t = schema.get("type")
    if t == "object":
        if not isinstance(x, dict):
            raise Invalide(f"{chemin} : objet attendu")
        props = schema.get("properties", {})
        inconnus = set(x) - set(props)
        if inconnus:
            raise Invalide(f"{chemin} : champs non autorisés {sorted(inconnus)} ; autorisés : {sorted(props)}")
        for k in schema.get("required", []):
            if k not in x:
                raise Invalide(f"{chemin} : champ requis manquant {k!r}")
        for k, v in x.items():
            valider(props[k], v, f"{chemin}.{k}")
    elif t == "array":
        if not isinstance(x, list):
            raise Invalide(f"{chemin} : liste attendue")
        if len(x) > schema.get("maxItems", MAX_LISTE):
            raise Invalide(f"{chemin} : au plus {schema.get('maxItems', MAX_LISTE)} éléments")
        for i, v in enumerate(x):
            valider(schema.get("items", {}), v, f"{chemin}[{i}]")
    elif t == "string":
        if not isinstance(x, str):
            raise Invalide(f"{chemin} : texte attendu")
        if len(x) > schema.get("maxLength", MAX_TEXTE):
            raise Invalide(f"{chemin} : texte trop long")
        if "enum" in schema and x not in schema["enum"]:
            raise Invalide(f"{chemin} : valeur {x!r} non autorisée ; valeurs : {schema['enum']}")
    elif t in ("number", "integer"):
        if isinstance(x, bool) or not isinstance(x, (int, float)) or (t == "integer" and not float(x).is_integer()):
            raise Invalide(f"{chemin} : {'entier' if t == 'integer' else 'nombre'} attendu")
        if x != x or x in (float("inf"), float("-inf")):
            raise Invalide(f"{chemin} : nombre invalide")
        if "enum" in schema and x not in schema["enum"]:
            raise Invalide(f"{chemin} : valeur non autorisée ; valeurs : {schema['enum']}")
        if "minimum" in schema and x < schema["minimum"] or "maximum" in schema and x > schema["maximum"]:
            raise Invalide(f"{chemin} : {x} hors bornes [{schema.get('minimum')} ; {schema.get('maximum')}]")
    elif t == "boolean":
        if not isinstance(x, bool):
            raise Invalide(f"{chemin} : booléen attendu")
    elif schema:
        raise Invalide(f"{chemin} : schéma non pris en charge")   # tout ce qui n'est pas prévu est refusé


def definitions() -> list[dict]:
    """Déclaration des outils pour le modèle de langage (format de l'API Messages)."""
    return [{"name": n, "description": d, "input_schema": s} for n, (d, s) in OUTILS.items()]

from ..model.relation import Relation


class StaticPumlFormatter(object):
    def __init__(self):
        pass

    def get_puml_for_model(self, classes, relations):
        result = '@startuml\n'
        for c in classes:
            result = result + "class {} {{\n".format(c.name)
            for m in c.methods:
                result = result + "    +{} {}()\n".format(m.return_type_name, m.name) # todo add arguments!
            result = result + "}\n"
        for r in relations:
            relation_as_uml = ""
            if r.type == Relation.USAGE:
                relation_as_uml = "{} --> {}: use\n".format(r.party_a, r.party_b)
            elif r.type == Relation.INHERITANCE:
                relation_as_uml = "{} <|-- {}\n".format(r.party_b, r.party_a)
            result = result + relation_as_uml
        result = result + "@enduml"
        return result

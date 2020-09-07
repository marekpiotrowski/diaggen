from ..model.relation import Relation


class StaticPumlFormatter(object):
    def __init__(self):
        pass

    @staticmethod
    def break_too_long_lines(lines):
        # todo naively break; later on, we have to detect whitespaces
        BREAK_AT = 60
        result_with_breaks = ""
        for i in range(len(lines.splitlines())):
            line = lines.splitlines()[i]
            line_with_breaks = '\\n'.join(line[i:i + BREAK_AT] for i in range(0, len(line), BREAK_AT))
            result_with_breaks = result_with_breaks + line_with_breaks + "\n"
        return result_with_breaks

    def get_puml_for_model(self, classes, relations):
        result = '@startuml\n'
        for c in classes:
            result = result + "class {} {{\n".format(c.name)
            for m in c.methods:
                args = ", ".join(m.arguments)
                result = result + "    +{} {}({})\n".format(m.return_type_name, m.name, args) # todo add arguments!
            result = result + "}\n"
        for r in relations:
            relation_as_uml = ""
            if r.type == Relation.USAGE:
                relation_as_uml = "{} --> {}: use\n".format(r.party_a, r.party_b)
            elif r.type == Relation.INHERITANCE:
                relation_as_uml = "{} <|-- {}\n".format(r.party_b, r.party_a)
            result = result + relation_as_uml
        result = result + "@enduml"
        result = self.break_too_long_lines(result)
        return result

import clang.cindex
from .model.class_metadata import ClassMetadata
from .model.method_metadata import MethodMetadata
from .model.relation import Relation


class CppTranslationUnitExtractor(object):
    def __init__(self, abs_filepath, abs_includes):
        self.__translation_unit_abs_filepath = abs_filepath
        self.__abs_includes = abs_includes
        self.__context = None
        self.__registered_classes = {}
        index = clang.cindex.Index.create()
        clang_args = ['-x', 'c++', '--std=c++14']  # TODO do something with args...
        includes = ["-I" + include for include in self.__abs_includes]
        clang_args = clang_args + includes
        self.__translation_unit = index.parse(self.__translation_unit_abs_filepath,
                                              args=clang_args)

    def get_classes(self):
        self.__context = None
        self.__registered_classes = {}
        self.__traverse_top_to_bottom()
        return list(self.__registered_classes.values())

    @staticmethod
    def demangle_relations(all_classes_big_picture):
        classes_ids = [c.name for c in all_classes_big_picture]
        relations = []
        for c in all_classes_big_picture:
            for m in c.methods:
                if (c.name not in m.return_type_name) and (m.return_type_name in classes_ids):
                    relation = Relation(c.name, m.return_type_name, Relation.USAGE)
                    relations.append(relation)
                for class_id in classes_ids:
                    if (c.name != class_id) and (class_id in ','.join(m.arguments)):
                        relation = Relation(c.name, class_id, Relation.USAGE)
                        relations.append(relation)
            for p in c.parents:
                relation = Relation(c.name, p, Relation.INHERITANCE)
                relations.append(relation)
        return relations

    @staticmethod
    def __is_exposed_field(node):
        return node.access_specifier == clang.cindex.AccessSpecifier.PUBLIC

    def __add_class_if_not_registered(self, node):
        if node is not None and node.kind in [clang.cindex.CursorKind.CLASS_DECL,
                                              clang.cindex.CursorKind.STRUCT_DECL] and \
                node.spelling not in self.__registered_classes:
            self.__registered_classes[node.spelling] = ClassMetadata(name=node.spelling, methods=[], parents=[])

    def __add_method_if_not_registered(self, new_node):
        if self.__context is None or new_node.kind not in [clang.cindex.CursorKind.CXX_METHOD,
                                                           clang.cindex.CursorKind.CONSTRUCTOR] \
                or not self.__is_exposed_field(new_node):
            return
        if self.__context.spelling not in self.__registered_classes:
            return
        if self.__registered_classes[self.__context.spelling].has_method(new_node.spelling):
            return
        arguments = [a.type.spelling for a in new_node.get_arguments()]
        method = MethodMetadata(name=new_node.spelling, arguments=arguments, return_type=new_node.result_type.spelling)
        self.__registered_classes[self.__context.spelling].add_method(method)

    def __add_parent_if_not_registered(self, new_node):
        if self.__context is None:
            return
        if new_node.kind != clang.cindex.CursorKind.CXX_BASE_SPECIFIER:
            return
        parent_name = new_node.spelling.split('::')[
            -1]  # for some reason, parent base specifier has full namespace information
        self.__registered_classes[self.__context.spelling].add_parent(parent_name)

    def __traverse_top_to_bottom(self):
        def classify(node):
            if self.__translation_unit_abs_filepath not in str(node.location):
                return
            if node.kind == clang.cindex.CursorKind.CLASS_DECL:
                self.__context = node
            self.__add_class_if_not_registered(self.__context)
            self.__add_method_if_not_registered(node)
            self.__add_parent_if_not_registered(node)
            # todo add fields!

        def visit(node, func):
            func(node)
            for c in node.get_children():
                visit(c, func)

        visit(self.__translation_unit.cursor, classify)

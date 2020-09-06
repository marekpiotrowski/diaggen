import clang.cindex
from .model.class_metadata import ClassMetadata
from .model.method_metadata import MethodMetadata


class CppTranslationUnitExtractor(object):
    def __init__(self, abs_filepath, abs_includes):
        self.__translation_unit_abs_filepath = abs_filepath
        self.__abs_includes = abs_includes
        self.__context = None
        self.__registered_classes = {}
        index = clang.cindex.Index.create()
        clang_args = ['-std=c++14']  # TODO do something with args...
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
        print(all_classes_big_picture)
        return []

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

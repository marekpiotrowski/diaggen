import clang.cindex
import typing
from .model.class_metadata import ClassMetadata
from .model.method_metadata import MethodMetadata


class CppTranslationUnitExtractor(object):
    def __init__(self, abs_filepath):
        self.__translation_unit_abs_filepath = abs_filepath

    def get_classes(self):
        index = clang.cindex.Index.create()
        translation_unit = index.parse(self.__translation_unit_abs_filepath,
                                       args=['-std=c++14'])
        all_classes = self.__filter_node_list_by_node_kind(translation_unit.cursor.get_children(),
                                                           [clang.cindex.CursorKind.CLASS_DECL,
                                                            clang.cindex.CursorKind.STRUCT_DECL],
                                                           go_into=[clang.cindex.CursorKind.NAMESPACE])

        result = []
        for c in all_classes:
            # print(dir(c))
            # self.__get_base_classes(c)
            # print(c.semantic_parent.spelling)
            methods_instances = self.__find_all_exposed_methods(c)
            class_instance = ClassMetadata(name=c.spelling, methods=methods_instances, parents=[])
            result.append(class_instance)
        # self.__demangle_relations()
        return result

    @staticmethod
    def __filter_node_list_by_node_kind(nodes, kinds, go_into):
        result = []
        for node in nodes:
            if node.kind in go_into:
                return CppTranslationUnitExtractor.__filter_node_list_by_node_kind(node.get_children(),
                                                                                   kinds, go_into)
            if node.kind in kinds:
                result.append(node)
        return result

    @staticmethod
    def __is_exposed_field(node):
        return node.access_specifier == clang.cindex.AccessSpecifier.PUBLIC

    @staticmethod
    def __find_all_exposed_methods(cursor):
        result = []
        field_declarations = CppTranslationUnitExtractor.__filter_node_list_by_node_kind(cursor.get_children(),
                                                                                         [
                                                                                             clang.cindex.CursorKind.CXX_METHOD],
                                                                                         go_into=[
                                                                                             clang.cindex.CursorKind.CLASS_DECL,
                                                                                             clang.cindex.CursorKind.STRUCT_DECL,
                                                                                             clang.cindex.CursorKind.NAMESPACE]
                                                                                         )
        for i in field_declarations:
            if not CppTranslationUnitExtractor.__is_exposed_field(i):
                continue
            arguments = [a.type.spelling for a in i.get_arguments()]
            result.append(MethodMetadata(name=i.spelling, arguments=arguments, return_type=i.result_type.spelling))
        return result

    def __demangle_relations(self):
        index = clang.cindex.Index.create()
        translation_unit = index.parse(self.__translation_unit_abs_filepath,
                                       args=['-std=c++14',
                                             "-I/diaggen/example/engine_controller/api"])  # TODO do something with args...
        base_specifiers = self.__filter_node_list_by_node_kind(translation_unit.cursor.get_children(),
                                                               [clang.cindex.CursorKind.CXX_BASE_SPECIFIER],
                                                               go_into=[clang.cindex.CursorKind.CLASS_DECL,
                                                                        clang.cindex.CursorKind.STRUCT_DECL,
                                                                        clang.cindex.CursorKind.NAMESPACE])
        for c in base_specifiers:
            # if c.kind == clang.cindex.CursorKind.CXX_BASE_SPECIFIER:
            print(c.spelling)

# def is_exposed_field(node):
#     return node.access_specifier == clang.cindex.AccessSpecifier.PUBLIC
#
#
# def find_all_exposed_fields(
#         cursor: clang.cindex.Cursor
# ):
#     result = []
#     field_declarations = filter_node_list_by_node_kind(cursor.get_children(), [clang.cindex.CursorKind.CXX_METHOD])
#     for i in field_declarations:
#         if not is_exposed_field(i):
#             continue
#         result.append(i.displayname)
#     return result
#
#
# def filter_node_list_by_node_kind(
#         nodes: typing.Iterable[clang.cindex.Cursor],
#         kinds: list
# ) -> typing.Iterable[clang.cindex.Cursor]:
#     result = []
#     for i in nodes:
#         # print(i.kind)
#         if i.kind == clang.cindex.CursorKind.NAMESPACE:
#             return filter_node_list_by_node_kind(i.get_children(), [clang.cindex.CursorKind.CLASS_DECL,
#                                                                     clang.cindex.CursorKind.STRUCT_DECL])
#         if i.kind in kinds:
#             result.append(i)
#     return result
#     # for i in nodes:
#     #     print(list(i.get_children()))
#     #     if i.kind in kinds:
#     #         result.append(i)
#
#
# all_classes = filter_node_list_by_node_kind(translation_unit.cursor.get_children(),
#                                             [clang.cindex.CursorKind.CLASS_DECL, clang.cindex.CursorKind.STRUCT_DECL])
# for i in all_classes:
#     print(i.spelling)
#     print(find_all_exposed_fields(i))

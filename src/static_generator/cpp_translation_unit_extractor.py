import clang.cindex
import typing
from .model.class_metadata import ClassMetadata

class CppTranslationUnitExtractor(object):
    def __init__(self, abs_filepath):
        self.__translation_unit_abs_filepath = abs_filepath

    def get_classes(self):
        index = clang.cindex.Index.create()
        translation_unit = index.parse(self.__translation_unit_abs_filepath,
                                       args=['-std=c++14'])  # TODO do something with args...
        all_classes = self.__filter_node_list_by_node_kind(translation_unit.cursor.get_children(),
                                                           [clang.cindex.CursorKind.CLASS_DECL,
                                                            clang.cindex.CursorKind.STRUCT_DECL])

        return [ClassMetadata(name=c.spelling) for c in all_classes]

    @staticmethod
    def __filter_node_list_by_node_kind(nodes, kinds):
        result = []
        for node in nodes:
            if node.kind == clang.cindex.CursorKind.NAMESPACE:
                return CppTranslationUnitExtractor.__filter_node_list_by_node_kind(node.get_children(),
                                                                                   [clang.cindex.CursorKind.CLASS_DECL,
                                                                                    clang.cindex.CursorKind.STRUCT_DECL])
            if node.kind in kinds:
                result.append(node)
        return result

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

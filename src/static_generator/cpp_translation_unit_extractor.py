import clang.cindex
from .model.class_metadata import ClassMetadata
from .model.method_metadata import MethodMetadata


class CppTranslationUnitExtractor(object):
    def __init__(self, abs_filepath, abs_includes):
        self.__translation_unit_abs_filepath = abs_filepath
        self.__abs_includes = abs_includes

    def get_classes(self):
        result = self.__traverse_top_to_bottom()
        return list(result.values())

    @staticmethod
    def __is_exposed_field(node):
        return node.access_specifier == clang.cindex.AccessSpecifier.PUBLIC

    def __traverse_top_to_bottom(self):
        index = clang.cindex.Index.create()
        clang_args = ['-std=c++14'] # TODO do something with args...
        includes = ["-I" + include for include in self.__abs_includes]
        clang_args = clang_args + includes
        translation_unit = index.parse(self.__translation_unit_abs_filepath,
                                       args=clang_args)
        context = {'$': None} # via dictionary, we need a mutable object
        registered_classes = {}

        def add_class_if_not_registered(node):
            if node is not None and node.kind in [clang.cindex.CursorKind.CLASS_DECL, clang.cindex.CursorKind.STRUCT_DECL] and \
                    node.spelling not in registered_classes:
                registered_classes[node.spelling] = ClassMetadata(name=node.spelling, methods=[], parents=[])

        def add_method_if_not_registered(new_node):
            if context['$'] is None or new_node.kind != clang.cindex.CursorKind.CXX_METHOD or not self.__is_exposed_field(new_node):
                return
            if context['$'].spelling not in registered_classes:
                return
            if registered_classes[context['$'].spelling].has_method(new_node.spelling):
                return
            arguments = [a.type.spelling for a in new_node.get_arguments()]
            method = MethodMetadata(name=new_node.spelling, arguments=arguments, return_type=new_node.result_type.spelling)
            registered_classes[context['$'].spelling].add_method(method)

        def add_parent_if_not_registered(new_node):
            if context['$'] is None:
                return
            if new_node.kind != clang.cindex.CursorKind.CXX_BASE_SPECIFIER:
                return
            parent_name = new_node.spelling.split('::')[-1] # for some reason, parent base specifier has full namespace information
            registered_classes[context['$'].spelling].add_parent(parent_name)

        def printall_visitor(node):
            if node.kind == clang.cindex.CursorKind.CLASS_DECL:
                context['$'] = node
            add_class_if_not_registered(context['$'])
            add_method_if_not_registered(node)
            add_parent_if_not_registered(node)
            #if node.kind in [clang.cindex.CursorKind.CLASS_DECL, clang.cindex.CursorKind.CXX_BASE_SPECIFIER]:
            #    print('Found grammar element "%s" {%s} [line=%s, col=%s]' % (node.displayname, node.kind, node.location.line, node.location.column))

        def visit(node, func):
            func(node)
            for c in node.get_children():
                visit(c, func)

        visit(translation_unit.cursor, printall_visitor)
        # print(registered_classes)
        return registered_classes
        # base_specifiers = self.__filter_node_list_by_node_kind(translation_unit.cursor.get_children(),
        #                                                        [clang.cindex.CursorKind.CXX_BASE_SPECIFIER],
        #                                                        go_into=[clang.cindex.CursorKind.CLASS_DECL,
        #                                                                 clang.cindex.CursorKind.STRUCT_DECL,
        #                                                                 clang.cindex.CursorKind.NAMESPACE])
        # for c in base_specifiers:
        #     # if c.kind == clang.cindex.CursorKind.CXX_BASE_SPECIFIER:
        #     print(c.spelling)

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

# lil helper!
# import clang.cindex
#
# index = clang.cindex.Index.create()
# tu = index.parse(sys.argv[1], args=["-std=c++98"], options=clang.cindex.TranslationUnit.PARSE_SKIP_FUNCTION_BODIES)
#
# def printall_visitor(node):
#     print 'Found grammar element "%s" {%s} [line=%s, col=%s]' % (node.displayname, node.kind, node.location.line, node.location.column)
#
# def visit(node, func):
#     func(node)
#     for c in node.get_children():
#         visit(c, func)
#
# visit(tu.cursor, printall_visitor)

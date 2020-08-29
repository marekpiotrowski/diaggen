import clang.cindex
import typing
index = clang.cindex.Index.create()
translation_unit = index.parse('example/engine_controller/api/engine_controller/ecu.h', args=['-std=c++14'])

def is_exposed_field(node):
    return node.access_specifier == clang.cindex.AccessSpecifier.PUBLIC

def find_all_exposed_fields(
    cursor: clang.cindex.Cursor
):
    result = []
    field_declarations = filter_node_list_by_node_kind(cursor.get_children(), [clang.cindex.CursorKind.CXX_METHOD])
    for i in field_declarations:
        if not is_exposed_field(i):
            continue
        result.append(i.displayname)
    return result

def filter_node_list_by_node_kind(
    nodes: typing.Iterable[clang.cindex.Cursor],
    kinds: list
) -> typing.Iterable[clang.cindex.Cursor]:
    result = []
    for i in nodes:
        #print(i.kind)
        if i.kind == clang.cindex.CursorKind.NAMESPACE:
            return filter_node_list_by_node_kind(i.get_children(), [clang.cindex.CursorKind.CLASS_DECL, clang.cindex.CursorKind.STRUCT_DECL])
        if i.kind in kinds:
            result.append(i)
    return result
    # for i in nodes:
    #     print(list(i.get_children()))
    #     if i.kind in kinds:
    #         result.append(i)
all_classes = filter_node_list_by_node_kind(translation_unit.cursor.get_children(), [clang.cindex.CursorKind.CLASS_DECL, clang.cindex.CursorKind.STRUCT_DECL])
for i in all_classes:
    print(i.spelling)
    print(find_all_exposed_fields(i))
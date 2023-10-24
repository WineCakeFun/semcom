from owlready2 import *
import codecs



global __DomOnto
global __ScenOnto
incompatibilities = []


def __check_semantic_compatibility(step_id):
    data_instances = []
    if __ScenOnto.messageFlow in __ScenOnto.classes():
        data_instances.extend(__ScenOnto.get_instances_of(__ScenOnto.messageFlow))
    if __ScenOnto.dataObject in __ScenOnto.classes():
        data_instances.extend(__ScenOnto.get_instances_of(__ScenOnto.dataObject))
    # if __ScenOnto.sequenceFlow in __ScenOnto.classes():
    #     data_instances.extend(__ScenOnto.get_instances_of(__ScenOnto.sequenceFlow))
        

    if len(data_instances) != 0:
        element_names = [targetRel[0] for targetRel in __ScenOnto.targetRef.get_relations() if
                         targetRel[1] == step_id and targetRel[0] in data_instances]

        # data_element_names = [element_name for element_name in element_names if element_name in data_instances]
        if len(element_names) == 0:
            return
        else:
            class_name = [nameRel[1] for nameRel in __ScenOnto["name"].get_relations() if nameRel[0] == element_names[0]][0]
            formatted_class_name = '_'.join(class_name.split(' '))

            if formatted_class_name not in [class_name.name.split('.')[0] for class_name in __DomOnto.classes()]:
                incompatibilities.append((formatted_class_name, element_names[0].name))


def process(scenario_path, pro_path):
    global __DomOnto
    global __ScenOnto
    __DomOnto = get_ontology(pro_path).load()
    __ScenOnto = get_ontology(scenario_path).load()

    current_id = get_start_id()

    __process_steps([current_id], [])



def __process_steps(steps_ids, visited_ids):
    if len(steps_ids) == 0:
        return

    for step_id in steps_ids:
        print([idRel[0] for idRel in __ScenOnto.id.get_relations() if idRel[1] == step_id])
        visited_ids.append(step_id)
        __check_semantic_compatibility(step_id)

        if [idRel[0] for idRel in __ScenOnto.id.get_relations() if idRel[1] == step_id][0] in __ScenOnto.get_instances_of(__ScenOnto.endEvent):
            return
        else:
            __process_steps([step for step in next_step(step_id) if step not in visited_ids], visited_ids)


def get_start_id():
    start_events = __ScenOnto.get_instances_of(__ScenOnto.startEvent)
    not_source_names = [idRel[0] for idRel in __ScenOnto.id.get_relations() if idRel[1] not in [sourceRel[1] for sourceRel in __ScenOnto.targetRef.get_relations()]]
    start_name = [start_event for start_event in start_events if start_event in not_source_names][0]
    start_id = [idRel[1] for idRel in __ScenOnto.id.get_relations() if idRel[0] == start_name][0]

    return start_id


def next_step(current_step_id):
    sequence_flow_names = [sourceRel[0] for sourceRel in __ScenOnto.sourceRef.get_relations()
                           if sourceRel[1] == current_step_id]

    target_ids = [targetRel[1] for targetRel in __ScenOnto.targetRef.get_relations() if targetRel[0] in sequence_flow_names]

    return target_ids

def export_incompatibilities_to_file(filename):
    with codecs.open(filename, 'w', encoding='utf-8') as f:
        f.write("Знайдено семантичну несумісність!:\n")
        for incompatibility in incompatibilities:
            f.write(f"Тип даних \"'{incompatibility[0]}'\", що використовується в елементі \"'{incompatibility[1]}'\", не знайдено в онтології.\n")


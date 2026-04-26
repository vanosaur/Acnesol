from agent.state import PipelineState
def run_image_node(state: PipelineState, model) -> PipelineState:
    from tools.image_tool import predict_acne_type, severity_map
    
    if state.manual_type_override:
        state.predicted_class = state.manual_type_override
        state.image_result = severity_map.get(state.manual_type_override, "Moderate")
        state.confidence_label = "Manual Override"
        return state

    if state.image is None:
        return state

    label, severity, confidence, all_scores = predict_acne_type(model, state.image)
    state.predicted_class = label
    state.image_result = severity
    state.image_confidence = confidence
    state.all_predictions = all_scores

    if confidence >= 0.75:
        state.confidence_label = "High"
    elif confidence >= 0.50:
        state.confidence_label = "Medium"
    else:
        state.confidence_label = "Low"

    return state

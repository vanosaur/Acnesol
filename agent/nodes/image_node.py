from agent.state import PipelineState
def run_image_node(state: PipelineState, model) -> PipelineState:
    from tools.image_tool import predict_acne_type
    
    if state.image is None:
        return state

    label, severity, confidence = predict_acne_type(model, state.image)
    state.predicted_class = label
    state.image_result = severity
    state.image_confidence = confidence

    if confidence >= 0.75:
        state.confidence_label = "High"
    elif confidence >= 0.50:
        state.confidence_label = "Medium"
    else:
        state.confidence_label = "Low"

    return state

"""
FastHTML Auto-Save Form Components Demo
Demonstrates various form components with automatic saving functionality
"""

# --- Imports ---
from fasthtml.common import *
from fasthtml.components import *
from monsterui.all import *  # Includes LabelRadio and LabelCheckboxX
from fastcore.basics import AttrDict

# --- Global Configuration ---
# Form field options
priority_options = ["Low", "Medium", "High"]
tag_options = ["important", "test", "draft", "urgent", "review"]
category_options = ["development", "design", "marketing", "research"]

# Test data
test_item = AttrDict(
    id=1,
    name="Test Item",
    description="This is a test description",
    status="Active",
    priority="Medium",
    tags=["important", "test"],
    category="development",
    steps=["Step 1", "Step 2", "Step 3"]
)

# Create app with blue theme and sortable support
app, rt = fast_app(None, hdrs=(
    Theme.blue.headers(),
    SortableJS('.sortable', ghost_class='blue-background-class')
), live=True)

# --- Component Render Functions ---
def render_auto_save_field(item_id, field_name, value, label, input_type="input"):
    """Render a basic input or textarea field with auto-save functionality
    Args:
        item_id: ID of the item being edited
        field_name: Name of the field (e.g., 'name', 'description')
        value: Current field value
        label: Display label for the field
        input_type: Either 'input' or 'textarea'
    """
    field_id = f"item-{field_name}-{item_id}"
    input_name = f"{field_name}_text"
    
    input_comp = (LabelTextArea(label, 
                               id=input_name,
                               name=input_name,
                               value=value,
                               cls="uk-width-1-1") 
                  if input_type == "textarea" 
                  else LabelInput(label, 
                                id=input_name,
                                name=input_name,
                                value=value,
                                cls="uk-width-1-1"))
    
    return Div(
        Form(
            input_comp,
            Hidden(name="item_id", value=item_id),
            Div(
                Span("Saving...", cls="uk-text-muted"),
                cls="htmx-indicator"
            ),
            **{
                'hx-put': f'/item/{item_id}/field/{field_name}',
                'hx-trigger': 'change',
                'hx-target': f'#{field_id}',
                'hx-swap': 'outerHTML',
                'hx-indicator': '.htmx-indicator'
            }
        ),
        cls="uk-margin-small",
        id=field_id
    )

def render_auto_save_dropdown(item_id, field_name, value, label, options):
    """Render a dropdown select with auto-save functionality
    Args:
        item_id: ID of the item being edited
        field_name: Name of the field (e.g., 'priority')
        value: Currently selected value
        label: Display label for the field
        options: List of possible values
    """
    field_id = f"item-{field_name}-{item_id}"
    input_name = f"{field_name}_text"
    
    return Div(
        Form(
            Label(label),
            Select(
                *[Option(opt, selected=(opt==value)) for opt in options],
                id=input_name,
                name=input_name,
                cls="uk-select"
            ),
            Hidden(name="item_id", value=item_id),
            Div(
                Span("Saving...", cls="uk-text-muted"),
                cls="htmx-indicator"
            ),
            **{
                'hx-put': f'/item/{item_id}/field/{field_name}',
                'hx-trigger': 'change',
                'hx-target': f'#{field_id}',
                'hx-swap': 'outerHTML',
                'hx-indicator': '.htmx-indicator'
            }
        ),
        cls="uk-margin-small",
        id=field_id
    )

def render_auto_save_multiselect(item_id, field_name, values, label, options):
    """Render a group of checkboxes for multiple selection with auto-save
    Args:
        item_id: ID of the item being edited
        field_name: Name of the field (e.g., 'tags')
        values: List of currently selected values
        label: Display label for the field
        options: List of all possible values
    """
    field_id = f"item-{field_name}-{item_id}"
    
    checkbox_group = Div(
        *[LabelCheckboxX(opt,
                        id=f"{field_name}_{i}",
                        name=f"{field_name}_text",
                        value=opt,
                        checked=(opt in values))
          for i, opt in enumerate(options)],
        cls="uk-margin-small"
    )
    
    return Div(
        Form(
            FormLabel(label),
            checkbox_group,
            Hidden(name="item_id", value=item_id),
            Div(
                Span("Saving...", cls="uk-text-muted"),
                cls="htmx-indicator"
            ),
            **{
                'hx-put': f'/item/{item_id}/field/{field_name}',
                'hx-trigger': 'change',
                'hx-target': f'#{field_id}',
                'hx-swap': 'outerHTML',
                'hx-indicator': '.htmx-indicator'
            }
        ),
        cls="uk-margin-small",
        id=field_id
    )

def render_auto_save_radio(item_id, field_name, value, label, options):
    """Render a group of radio buttons with auto-save
    Args:
        item_id: ID of the item being edited
        field_name: Name of the field (e.g., 'category')
        value: Currently selected value
        label: Display label for the field
        options: List of possible values
    """
    field_id = f"item-{field_name}-{item_id}"
    
    radio_buttons = [
        LabelRadio(
            label=opt,
            id=f"{field_name}_{i}",
            name=f"{field_name}_text",
            value=opt,
            checked=(opt == value),
            cls="uk-margin-small"
        )
        for i, opt in enumerate(options)
    ]
    
    return Div(
        Form(
            Label(label, cls="uk-form-label"),
            Div(*radio_buttons, cls="uk-margin-small"),
            Hidden(name="item_id", value=item_id),
            Div(
                Span("Saving...", cls="uk-text-muted"),
                cls="htmx-indicator"
            ),
            **{
                'hx-put': f'/item/{item_id}/field/{field_name}',
                'hx-trigger': 'change',
                'hx-target': f'#{field_id}',
                'hx-swap': 'outerHTML',
                'hx-indicator': '.htmx-indicator'
            }
        ),
        cls="uk-margin-small",
        id=field_id
    )

def render_auto_save_sortable(item_id, field_name, values, label):
    """Render a sortable list with auto-save
    Args:
        item_id: ID of the item being edited
        field_name: Name of the field (e.g., 'steps')
        values: List of values in current order
        label: Display label for the field
    """
    field_id = f"item-{field_name}-{item_id}"
    
    list_items = [
        Li(
            Div(
                Span("☰", cls="uk-margin-small-right"),  # Drag handle
                Span(value),
                Hidden(name=f"{field_name}_text", value=value),
                cls="uk-flex uk-flex-middle"
            ),
            id=f"item-{i}",
            cls="uk-padding-small uk-background-muted uk-margin-small"
        )
        for i, value in enumerate(values)
    ]
    
    return Div(
        Form(
            Label(label, cls="uk-form-label"),
            Ul(
                *list_items,
                cls="sortable uk-list uk-padding-small",
                **{
                    'hx-post': f'/item/{item_id}/sort/{field_name}',
                    'hx-trigger': 'end',
                    'hx-target': f'#{field_id}',
                    'hx-swap': 'outerHTML'
                }
            ),
            Hidden(name="item_id", value=item_id),
            Div(
                Span("Saving order...", cls="uk-text-muted"),
                cls="htmx-indicator"
            ),
            id=field_id
        ),
        cls="uk-margin",
        id=field_id
    )

# --- Page Rendering ---
def render_test_page():
    """Render the main page with all auto-save form components"""
    return Div(
        # Page header
        H1("Auto-Save Fields Demo", cls="uk-heading-medium"),
        P("Edit any field below - they will save automatically when changed.", 
          cls="uk-text-muted"),
        
        # Form container
        Div(
            # Text input fields
            render_auto_save_field(1, "name", test_item.name, "Item Name"),
            render_auto_save_field(1, "description", test_item.description, 
                                 "Description", "textarea"),
            render_auto_save_field(1, "status", test_item.status, "Status"),
            
            # Selection fields
            render_auto_save_dropdown(1, "priority", test_item.priority, 
                                   "Priority", priority_options),
            render_auto_save_multiselect(1, "tags", test_item.tags, 
                                       "Tags", tag_options),
            render_auto_save_radio(1, "category", test_item.category, 
                                 "Category", category_options),
            
            # Sortable list
            render_auto_save_sortable(1, "steps", test_item.steps, "Steps"),
            
            cls="uk-margin-medium-top uk-flex uk-flex-column"
        ),
        cls="uk-container uk-margin-top",
        id="main-content"
    )

# --- Route Handlers ---
@rt('/')
def get(req):
    """Main page route handler"""
    return render_test_page()



@rt('/item/{item_id}/field/{field_name}', methods=['PUT'])
async def put(req):
    """Handle updates for individual form fields
    
    Supports different field types:
    - Basic inputs and textareas
    - Dropdown selects
    - Multi-select checkboxes
    - Radio button groups
    """
    try:
        item_id = int(req.path_params['item_id'])
        field_name = req.path_params['field_name']
        form = await req.form()
        input_name = f"{field_name}_text"
        
        # Handle single-value fields validation
        if input_name not in form and field_name != "tags":
            return "Missing field value", 400
            
        # Handle field types in form order
        if field_name in ["name", "status"]:
            new_value = form[input_name].strip()
            if not new_value:
                return "Empty value not allowed", 400
            setattr(test_item, field_name, new_value)
            return render_auto_save_field(
                test_item.id,
                field_name,
                new_value,
                field_name.replace('_', ' ').title(),
                "input"
            )
            
        elif field_name == "description":
            new_value = form[input_name].strip()
            if not new_value:
                return "Empty value not allowed", 400
            setattr(test_item, field_name, new_value)
            return render_auto_save_field(
                test_item.id,
                field_name,
                new_value,
                field_name.replace('_', ' ').title(),
                "textarea"
            )
            
        elif field_name == "priority":
            new_value = form[input_name].strip()
            if not new_value:
                return "Empty value not allowed", 400
            setattr(test_item, field_name, new_value)
            return render_auto_save_dropdown(
                test_item.id,
                field_name,
                new_value,
                field_name.replace('_', ' ').title(),
                priority_options
            )
            
        elif field_name == "tags":
            new_values = form.getlist(input_name)
            setattr(test_item, field_name, new_values)
            return render_auto_save_multiselect(
                test_item.id,
                field_name,
                new_values,
                field_name.replace('_', ' ').title(),
                tag_options
            )
            
        elif field_name == "category":
            new_value = form[input_name].strip()
            if not new_value:
                return "Empty value not allowed", 400
            setattr(test_item, field_name, new_value)
            return render_auto_save_radio(
                test_item.id,
                field_name,
                new_value,
                field_name.replace('_', ' ').title(),
                category_options
            )
            
    except Exception as e:
        print(f"Error updating field: {e}")
        return "Server error", 500




@rt('/item/{item_id}/sort/{field_name}', methods=['POST'])
async def post(req):
    """Handle reordering of sortable lists"""
    try:
        item_id = int(req.path_params['item_id'])
        field_name = req.path_params['field_name']
        
        form = await req.form()
        new_values = form.getlist(f"{field_name}_text")
        
        # Update the item with the new order
        setattr(test_item, field_name, new_values)
        
        # Return the updated sortable component
        return render_auto_save_sortable(
            item_id,
            field_name,
            new_values,
            field_name.replace('_', ' ').title()
        )
            
    except Exception as e:
        print(f"Error updating sort order: {e}")
        return "Server error", 500

# --- Main Entry Point ---
if __name__ == '__main__':
    serve()

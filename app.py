import streamlit as st
from datetime import datetime, date, time as dtime
from pawpal_system import Task, Pet, Owner, Scheduler, Priority

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# ── Session state bootstrap ───────────────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = None

if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

# ── Section 1: Owner setup ────────────────────────────────────────────────────
st.header("Owner")

if st.session_state.owner is None:
    with st.form("owner_form"):
        owner_name    = st.text_input("Your name")
        owner_address = st.text_input("Your address")
        submitted     = st.form_submit_button("Create owner")

    if submitted:
        if not owner_name.strip():
            st.warning("Name is required.")
        else:
            st.session_state.owner     = Owner(name=owner_name.strip(),
                                               address=owner_address.strip())
            st.session_state.scheduler = Scheduler(st.session_state.owner)
            st.rerun()
else:
    owner = st.session_state.owner
    st.success(f"**{owner.name}** — {owner.address}")
    if st.button("Reset (clears all data)"):
        st.session_state.owner     = None
        st.session_state.scheduler = None
        st.rerun()

# Stop rendering until an owner exists
if st.session_state.owner is None:
    st.stop()

owner     = st.session_state.owner
scheduler = st.session_state.scheduler
assert isinstance(owner, Owner) and isinstance(scheduler, Scheduler)

st.divider()

# ── Section 2: Pets ───────────────────────────────────────────────────────────
st.header("Pets")

if owner.pets:
    for pet in owner.pets:
        st.markdown(f"- **{pet.name}** ({pet.species} · {pet.breed} · age {pet.age})")
else:
    st.info("No pets yet — add one below.")

with st.expander("Add a new pet"):
    with st.form("pet_form"):
        pet_name    = st.text_input("Pet name")
        col1, col2  = st.columns(2)
        with col1:
            pet_species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Rabbit", "Other"])
            pet_age     = st.number_input("Age (years)", min_value=0, max_value=30, value=1)
        with col2:
            pet_breed   = st.text_input("Breed")
        add_pet = st.form_submit_button("Add pet")

    if add_pet:
        if not pet_name.strip():
            st.warning("Pet name is required.")
        elif pet_name.strip() in [p.name for p in owner.pets]:
            st.warning(f"A pet named '{pet_name.strip()}' already exists.")
        else:
            owner.addPet(Pet(
                name    = pet_name.strip(),
                species = pet_species,
                breed   = pet_breed.strip() or "Unknown",
                age     = int(pet_age),
            ))
            st.rerun()

# Stop rendering task section until at least one pet exists
if not owner.pets:
    st.stop()

st.divider()

# ── Section 3: Add task ───────────────────────────────────────────────────────
st.header("Add Task")

pet_names = [p.name for p in owner.pets]

with st.form("task_form"):
    selected_pet  = st.selectbox("Assign to", pet_names)
    task_title    = st.text_input("Task title")
    col1, col2, col3 = st.columns(3)
    with col1:
        task_date = st.date_input("Date", value=date.today())
    with col2:
        task_time = st.time_input("Time", value=dtime(8, 0))
    with col3:
        task_duration = st.number_input("Duration (min)", min_value=1, max_value=480, value=30)
    task_priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
    add_task = st.form_submit_button("Add task")

if add_task:
    if not task_title.strip():
        st.warning("Task title is required.")
    else:
        scheduler.schedule_task(
            selected_pet,
            Task(
                title            = task_title.strip(),
                time             = datetime.combine(task_date, task_time),
                duration_minutes = int(task_duration),
                priority         = Priority(task_priority),
            ),
        )
        st.rerun()

st.divider()

# ── Section 4: Schedule ───────────────────────────────────────────────────────
st.header("Schedule")

all_tasks = scheduler.get_all_tasks()

if not all_tasks:
    st.info("No tasks scheduled yet.")
else:
    for pet in owner.pets:
        if not pet.tasks:
            continue
        st.subheader(pet.name)
        for task in sorted(pet.tasks, key=lambda t: t.time):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                label = f"~~{task.title}~~" if task.completed else task.title
                st.markdown(
                    f"{label} — {task.time.strftime('%b %d, %H:%M')} · "
                    f"{task.duration_minutes} min · `{task.priority.value}`"
                )
            with col2:
                st.caption("done" if task.completed else "pending")
            with col3:
                if not task.completed:
                    if st.button("Complete", key=f"done_{task.id}"):
                        scheduler.complete_task(task.id)
                        st.rerun()

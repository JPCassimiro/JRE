from shared_ui_modules.modules.db_functions import SharedDbClass

class DbClass(SharedDbClass):
    def __init__(self, parent = None):
        super().__init__()

        self.initialize_module()
    
    #send string wihtou db
    def get_db_name(self):
        return "jre"
    
    def get_query_list(self):
        return ["""
            create table if not exists therapist (
                id integer primary key,
                name text not null,
                details text not null,
                image_path text
            );""","""
            create table if not exists patient(
                id integer primary key,
                name text not null,
                details text not null,
                image_path text
            );""","""
            create table if not exists session (
                id integer primary key,
                patient_id integer not null,
                session_date timestamp not null default current_timestamp,
                foreign key (patient_id) references patient(id) on delete cascade
            );""","""
            create table if not exists use_data (
                id integer primary key,
                session_id integer not null,
                action text check(action in ('inhale','exhale')),
                pressure integer not null,
                timestamp datetime default current_timestamp,
                foreign key (session_id) references session(id) on delete cascade
            );""","""
            create table if not exists game_profile (
                id integer primary key,
                patient_id integer not null,
                name text not null,
                foreign key (patient_id) references patient(id) on delete cascade
            );""","""
            create table if not exists bindings (
                id integer primary key,
                game_id integer not null,
                bindings_json text not null,
                foreign key (game_id) references game_profile(id) on delete cascade
            );""","""insert into patient (id, name, details, image_path)
            values (1, 'paciente padrão', 'valor padrão', '_internal/resources/imgs/placeholder_profile.png');""","""insert into therapist (id, name, details, image_path)
            values (1, 'terapeuta padrão', 'valor padrão', '_internal/resources/imgs/placeholder_profile.png');"""]

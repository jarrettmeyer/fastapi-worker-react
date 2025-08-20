create table public.tasks (
  task_id uuid not null,
  descr character varying(2000) not null,
  created_ts timestamp with time zone not null,
  updated_ts timestamp with time zone not null,
  status character varying(200) not null,
  constraint tasks_pkey primary key (task_id)
);

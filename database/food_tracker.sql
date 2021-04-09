create table dates (
    id         integer primary key autoincrement,
    entry_date date    not null
) ;

create table foods (
    id         integer primary key autoincrement,
    name       text    not null,
    protein    integer not null,
    carbs      integer not null,
    fat        integer not null,
    calories   integer not null
) ;

create table daily_intake (
    date_id    integer not null,
    food_id    integer not null,
    primary key (date_id, food_id)
) ;

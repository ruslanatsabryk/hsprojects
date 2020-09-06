import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()


class TaskTable(Base):
    __tablename__ = 'task'
    id = sa.Column(sa.Integer, primary_key=True)
    task = sa.Column(sa.String)
    deadline = sa.Column(sa.Date, default=datetime.today())

    def __repr__(self):
        return self.task


engine = sa.create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)
Session = sa.orm.sessionmaker(bind=engine)
session = Session()

menu = ["1) Today's tasks\n", "2) Week's tasks\n", "3) All tasks\n",
        "4) Missed tasks\n", "5) Add task\n", "6) Delete task\n", "0) Exit\n", ]
while True:
    menu_item = input("".join(menu))
    if menu_item == '1':
        today = datetime.today()
        rows = session.query(TaskTable).filter(TaskTable.deadline == today.date()).all()
        print(f'\nToday {today.date().strftime("%#d %b")}:')
        if len(rows) > 0:
            print(*[str(num) + '. ' + str(row) for num, row in enumerate(rows, 1)], sep='\n', end='\n\n')
        else:
            print('Nothing to do!\n')
    elif menu_item == '2':
        print()
        for d in range(7):
            next_date = datetime.today() + timedelta(days=d)
            rows = session.query(TaskTable).filter(TaskTable.deadline == next_date.date()).all()
            print(f'{next_date.strftime("%A %#d %b")}:')
            if len(rows) > 0:
                print(*[str(num) + '. ' + str(row) for num, row in enumerate(rows, 1)], sep='\n', end='\n\n')
            else:
                print('Nothing to do!\n')
    elif menu_item == '3':
        rows = session.query(TaskTable).order_by(TaskTable.deadline).all()
        print('\nAll tasks:', *[str(num) + '. ' + str(row.task) + '. ' + datetime.strptime(str(row.deadline),
                '%Y-%m-%d').strftime('%#d %b') for num, row in enumerate(rows, 1)], sep='\n', end='\n\n')
    elif menu_item == '4':
        rows = session.query(TaskTable).\
            filter(TaskTable.deadline < datetime.today().date()).order_by(TaskTable.deadline).all()
        print('\nMissed tasks:')
        if len(rows) > 0:
            print(*[str(num) + '. ' + str(row.task) + '. ' + datetime.strptime(str(row.deadline),
                  '%Y-%m-%d').strftime('%#d %b') for num, row in enumerate(rows, 1)], sep='\n', end='\n\n')
        else:
            print('Nothing is missed!\n')
    elif menu_item == '5':
        task = input('\nEnter task\n')
        deadline = datetime.strptime(input('Enter deadline\n'), '%Y-%m-%d')
        new_row = TaskTable(task=task, deadline=deadline)
        session.add(new_row)
        session.commit()
        print()
    elif menu_item == '6':
        rows = session.query(TaskTable). \
            filter(TaskTable.deadline <= datetime.today().date()).order_by(TaskTable.deadline).all()
        if len(rows) > 0:
            missed_tasks = [str(num) + '. ' + str(row.task) + '. ' + datetime.strptime(str(row.deadline), '%Y-%m-%d').
                        strftime('%#d %b') for num, row in enumerate(rows, 1)]
            print('\nChoose the number of the task you want to delete:', *missed_tasks, sep='\n', end='\n')
            to_delete = int(input())
            session.delete(rows[to_delete - 1])
            session.commit()
            print('The task has been deleted!\n')
        else:
            print('\nNothing to delete\n')
    else:
        print('\nBye!')
        break

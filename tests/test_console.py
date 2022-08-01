import unittest
from unittest.mock import patch
import console
from io import StringIO
from re import search
import os


class Tests_Console(unittest.TestCase):

    def test_destroy(self):
        id = ""
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("create User")
            id = f.getvalue()[0:-1]
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().precmd("User.count()")
            self.assertEqual('1', f.getvalue()[0:-1])
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd(f"destroy User {id}")
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().precmd("User.count()")
            self.assertEqual('0', f.getvalue()[0:-1])

    def test_help(self):
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("help show")
            self.assertEqual(f.getvalue(), """Usage: show <class_name> <id>\n
show: Show an instance with the id\n""")

    def test_help_all(self):
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("help all")
            self.assertEqual(f.getvalue(), """Usage: all <BaseModel> | all
all: Display all instances or specific one\n""")

    def test_help_quit(self):
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("help quit")
            self.assertEqual(f.getvalue(), """Usage: quit,\n
quits the shell\n""")

    def test_help_EOF(self):
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("help EOF")
            self.assertEqual(f.getvalue(), """Usage: EOF or CTRL+D\n
quits the shell\n""")

    def test_help_create(self):
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("help create")
            self.assertEqual(f.getvalue(), """Usage: create <class_name>
create: Create a new instance of a class\n""")

    def test_help_destroy(self):
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("help destroy")
            self.assertEqual(f.getvalue(), """Usage: destroy <class_name> <id>
destroy: Destroy an instance with the id\n""")

    def test_help_update(self):
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("help update")
            self.assertEqual(f.getvalue(), """Usage: update <class name> <id>
 <attr name> <attr value>
update: changes or adds an attribute to an instance\n""")

    def test_create(self):
        regex = r"^[\da-f]{8}-(?:[\da-f]{4}-){3}[\da-f]{12}\n$"
        id = ""
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("create User")
            id = f.getvalue()
            self.assertEqual(f.getvalue(), search(regex, id).string)
            console.HBNBCommand().onecmd(f"destroy User {id}")

        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("create")
            self.assertEqual(f.getvalue(), "** class name missing **\n")

        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("create zzz")
            self.assertEqual(f.getvalue(), "** class doesn't exist **\n")

        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("create Place")
            id = f.getvalue()
            self.assertEqual(f.getvalue(), search(regex, id).string)
            console.HBNBCommand().onecmd(f"destroy Place {id}")

    def test_show(self):
        id = ""
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("create User")
            id = f.getvalue()[0:-1]
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd(f"show User {id}")
            self.assertIn(id, f.getvalue())
            console.HBNBCommand().onecmd(f"destroy User {id}")

        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd(f"show User")
            self.assertEqual(f.getvalue(), "** instance id missing **\n")
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd(f"show User zzz")
            self.assertEqual(f.getvalue(), "** no instance found **\n")

        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("create User")
            id = f.getvalue()[0:-1]
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd(f"User.show({id})")
            self.assertIn(id, f.getvalue())
            console.HBNBCommand().onecmd(f"destroy User {id}")

        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd(f"all")
            self.assertIn("[]", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().precmd(f"User.all()")
            self.assertIn("", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd(f"all asd")
            self.assertIn("** class doesn't exist **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("create User")
            id = f.getvalue()[0:-1]
            console.HBNBCommand().precmd(f"all User")
            self.assertIn(id, f.getvalue())
            console.HBNBCommand().onecmd(f"destroy User {id}")

    def test_update(self):
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("create User")
            id = f.getvalue()[0:-1]
            console.HBNBCommand().onecmd(f"update User {id} name GuyIncognito")
            console.HBNBCommand().onecmd(f"show User {id}")
            self.assertIn("name", f.getvalue())
            console.HBNBCommand().onecmd(f"destroy User {id}")

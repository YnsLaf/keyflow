import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from keyflow import command, uninstall


class UninstallTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_path_line_is_removed_and_rest_kept(self):
        rc = self.tmp / ".zshrc"
        rc.write_text("alias ll='ls -l'\n\n%s\nexport PATH=\"$PATH:/x/bin\"\nexport EDITOR=vim\n"
                      % command.MARKER, encoding="utf-8")
        with mock.patch.object(command, "_rc_file", return_value=rc):
            self.assertIsNotNone(uninstall.remove_path_line())
            self.assertIsNone(uninstall.remove_path_line())
        self.assertEqual(rc.read_text(encoding="utf-8"), "alias ll='ls -l'\nexport EDITOR=vim\n")

    def test_data_and_empty_folder_are_removed(self):
        folder = self.tmp / ".keyflow"
        folder.mkdir()
        data = folder / "data.json"
        data.write_text("{}", encoding="utf-8")
        (folder / "data.broken.json").write_text("{", encoding="utf-8")
        self.assertTrue(uninstall.remove_data(data))
        self.assertFalse(folder.exists())

    def test_data_folder_with_other_files_stays(self):
        data = self.tmp / "data.json"
        data.write_text("{}", encoding="utf-8")
        (self.tmp / "notes.txt").write_text("keep", encoding="utf-8")
        uninstall.remove_data(data)
        self.assertTrue((self.tmp / "notes.txt").exists())

    @unittest.skipIf(os.name == "nt", "symlinks")
    def test_only_the_keyflow_link_is_removed(self):
        scripts = self.tmp / "scripts"
        scripts.mkdir()
        bin_dir = self.tmp / "bin"
        bin_dir.mkdir()
        (bin_dir / "keyflow").symlink_to(scripts / "keyflow")
        (bin_dir / "other").symlink_to(scripts / "keyflow")
        with mock.patch.object(command, "_script_dirs", return_value=[scripts]), \
                mock.patch.dict(os.environ, {"PATH": str(bin_dir)}):
            self.assertEqual(uninstall.remove_command_link(), str(bin_dir / "keyflow"))
        self.assertFalse(os.path.lexists(str(bin_dir / "keyflow")))
        self.assertTrue(os.path.lexists(str(bin_dir / "other")))

    @unittest.skipIf(os.name == "nt", "symlinks")
    def test_foreign_keyflow_link_stays(self):
        bin_dir = self.tmp / "bin"
        bin_dir.mkdir()
        (bin_dir / "keyflow").symlink_to(self.tmp / "somewhere" / "keyflow")
        with mock.patch.object(command, "_script_dirs", return_value=[self.tmp / "scripts"]), \
                mock.patch.dict(os.environ, {"PATH": str(bin_dir)}):
            self.assertIsNone(uninstall.remove_command_link())
        self.assertTrue(os.path.lexists(str(bin_dir / "keyflow")))


if __name__ == "__main__":
    unittest.main()

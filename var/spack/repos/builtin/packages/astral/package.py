# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os.path


class Astral(Package):
    """ASTRAL is a tool for estimating an unrooted species tree given a set of
       unrooted gene trees."""

    homepage = "https://github.com/smirarab/ASTRAL"
    url      = "https://github.com/smirarab/ASTRAL/archive/v4.10.7.tar.gz"

    version('4.10.7', '38c81020570254e3f5c75d6c3c27fc6d')

    depends_on('java', type=('build', 'run'))
    depends_on('zip', type='build')

    phases = ['build', 'install']

    def build(self, spec, prefix):
        make = Executable('./make.sh')
        make()

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install_tree('lib', prefix.tools.lib)
        jar_file = 'astral.{v}.jar'.format(v=self.version)
        install(jar_file, prefix.tools)

        script_sh = join_path(os.path.dirname(__file__), "astral.sh")
        script = prefix.bin.astral
        install(script_sh, script)
        set_executable(script)

        java = self.spec['java'].prefix.bin.java
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('astral.jar', join_path(prefix.tools, jar_file),
                    script, **kwargs)

    def setup_environment(self, spack_env, run_env):
        run_env.set('ASTRAL_HOME', self.prefix.tools)

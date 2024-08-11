#! /usr/bin/env python
# encoding: utf-8
import os.path

def options(opt):
    opt.load('java')
    opt.recurse('jni')

def configure(conf):
    conf.load('java')
    conf.recurse('jni')

def build(bld):
    bld.recurse('jni')

    SAT4JREPO = 'https://repo1.maven.org/maven2/org/ow2/sat4j/org.ow2.sat4j.core/2.3.6/'
    bld(rule = 'wget ' + SAT4JREPO + '${TGT}',
        target = 'org.ow2.sat4j.core-2.3.6.jar')
    bld(rule = 'wget ' + SAT4JREPO + '${TGT}',
        target = 'org.ow2.sat4j.core-2.3.6-sources.jar')

    bld(rule = 'wget -O junit.jar "http://search.maven.org/remotecontent?filepath=junit/junit/4.12/junit-4.12.jar"',
        target = 'junit.jar')
    bld(rule = 'wget -O hamcrest-core.jar "http://search.maven.org/remotecontent?filepath=org/hamcrest/hamcrest-core/1.3/hamcrest-core-1.3.jar"',
        target = 'hamcrest-core.jar')

    bld.add_group()

    bld(features  = 'javac jar',
        name      = 'kodkod',
        srcdir    = 'src', 
        outdir    = 'kodkod',
        compat    = '1.8',
        classpath = ['.', 'org.ow2.sat4j.core-2.3.6.jar'],
        manifest  = 'src/MANIFEST',
        basedir   = 'kodkod',
        destfile  = 'kodkod.jar')
    
    bld(features  = 'javac jar',
        name      = 'examples',
        use       = 'kodkod',
        srcdir    = 'examples', 
        outdir    = 'examples',
        compat    = '1.8',
        classpath = ['.', 'kodkod.jar'],
        manifest  = 'examples/MANIFEST',
        basedir   = 'examples',
        destfile  = 'examples.jar')
    
    bld.install_files('${LIBDIR}', ['kodkod.jar', 'examples.jar'])

def distclean(ctx):
    from waflib import Scripting
    Scripting.distclean(ctx)
    ctx.recurse('jni')


from waflib.Build import BuildContext
class TestContext(BuildContext):
        cmd = 'test'
        fun = 'test'

def test(bld):
    """compiles and runs tests"""

    cp = ['.', 'kodkod.jar', 'examples.jar', 'org.ow2.sat4j.core-2.3.6.jar', 'junit.jar', 'hamcrest-core.jar']
    bld(features  = 'javac',
        name      = 'test',
        srcdir    = 'test',
        classpath = cp, 
        use       = ['kodkod', 'examples'])
    bld.add_group()

    bld(rule = 'java -cp {classpath} -Djava.library.path={libpath} {junit} {test}'.format(classpath = ':'.join(cp),
                                                                                          libpath = bld.env.LIBDIR,
                                                                                          junit = 'org.junit.runner.JUnitCore',
                                                                                          test = 'kodkod.test.AllTests'),
        always = True) 


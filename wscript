#! /usr/bin/env python
# encoding: utf-8
import os.path

SAT4J      = "org.ow2.sat4j.core"
SAT4J_VER  = "2.3.6"
SAT4J_REPO = "https://repo1.maven.org/maven2/org/ow2/sat4j/%s/%s/" % (SAT4J, SAT4J_VER)
SAT4J_JAR  = "%s-%s.jar" % (SAT4J, SAT4J_VER)
SAT4J_SRC  = "%s-%s-sources.jar" % (SAT4J, SAT4J_VER)

def options(opt):
    opt.load('java')
    opt.recurse('jni')

def configure(conf):
    conf.load('java')
    conf.recurse('jni')

def build(bld):
    bld.recurse('jni')

    bld(rule = 'wget ' + SAT4J_REPO + SAT4J_JAR,
        target = SAT4J_JAR)
    bld(rule = 'wget ' + SAT4J_REPO + SAT4J_SRC,
        target = SAT4J_SRC)

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
        classpath = ['.', SAT4J_JAR],
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
    
    bld.install_files('${LIBDIR}', [SAT4J_JAR, 'kodkod.jar', 'examples.jar'])

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

    cp = ['test', SAT4J_JAR, 'kodkod.jar', 'examples.jar', 'junit.jar', 'hamcrest-core.jar']
    bld(features  = 'javac',
        name      = 'test',
        srcdir    = 'test',
        outdir    = 'test',
        compat    = '1.8',
        classpath = cp, 
        use       = ['kodkod', 'examples'])
    bld.add_group()

    bld(rule = 'java -cp {classpath} -Djava.library.path={libpath} {junit} {test}'.format(classpath = ':'.join(cp),
                                                                                          libpath = bld.env.LIBDIR,
                                                                                          junit = 'org.junit.runner.JUnitCore',
                                                                                          test = 'kodkod.test.AllTests'),
        always = True) 


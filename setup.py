from setuptools import setup


def version_scheme(version):
    import setuptools_scm.version
    if version.exact:
        return setuptools_scm.version.guess_next_simple_semver(
            version.tag, retain=setuptools_scm.version.SEMVER_LEN, increment=False)
    else:
        return version.format_next_version(
            setuptools_scm.version.guess_next_simple_semver, retain=setuptools_scm.version.SEMVER_MINOR
        )


setup(
    use_scm_version={
        "version_scheme": version_scheme,
        "local_scheme": "no-local-version",
        "write_to": "ppc_asm/version.py",
    },
)

def test_can_import_modules():
    import probe.app
    import probe.authorization
    import probe.discovery
    import probe.dns_utils
    import probe.email_checks
    import probe.risk_engine
    import probe.tls_checks
    import probe.web_checks

    assert True

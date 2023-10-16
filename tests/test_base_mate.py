from multidb_models.base_meta import IdMongoMeta


def test_idMongoMeta():
    raw = {
        '_id': 'f82192c2460965cd0a9ce68305c1969a4'
    }
    data = IdMongoMeta(
        **raw
    )
    data_null = IdMongoMeta()
    print(data.id)
    print(data_null.id)
    assert(False)



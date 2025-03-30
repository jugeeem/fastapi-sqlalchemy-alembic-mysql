# !/usr/bin/python
# -*- coding: utf-8 -*-
"""ドメイン列挙型モジュール

このモジュールでは、ドメインで使用される様々な列挙型を定義します。
これらの列挙型は、型安全性の確保と、意味のある値の限定に使用されます。
"""

import enum


class Gender(enum.Enum):
    """性別の選択肢を定義する列挙型

    ユーザーの性別を表現するための列挙型です。
    データベースのカラム型や、APIでの入力値の検証に使用されます。

    Attributes:
        MALE (str): 男性を表す値。
        FEMALE (str): 女性を表す値。
    """

    MALE = "male"
    FEMALE = "female"


class Role(enum.Enum):
    """ユーザー権限レベルを定義する列挙型

    システム内のユーザーロール（権限グループ）を表す列挙型です。
    各ロールはアクセス制御に使用され、階層的な権限構造を持ちます。

    Attributes:
        ADMIN (str): システム管理者。最高レベルの権限を持ちます。
        MANAGER (str): 管理者。ユーザー管理や一部の管理機能にアクセスできます。
        USER (str): 一般ユーザー。標準的な機能にアクセスできます。
        GUEST (str): 閲覧のみユーザー。閲覧権限のみを持ちます。
    """

    ADMIN = "admin"  # システム管理者
    MANAGER = "manager"  # 管理者
    USER = "user"  # 一般ユーザ
    GUEST = "guest"  # 閲覧のみ

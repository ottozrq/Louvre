from tests import ApiClient, m, status
from src.routes.users import ResetPasswordRequest, ResetPasswordResponse


def test_user_register_flow(cl: ApiClient):
    user_email = "otto"
    password = "666666"
    user = m.User.from_response(
        cl(
            "/register/",
            method="POST",
            data=m.UserCreate(
                user_email=user_email,
                password=password,
            ),
        )
    )
    assert user.user_email == user_email
    assert (
        m.LoginResponse.from_response(
            cl(
                "/token/",
                method="POST",
                data={"password": password, "username": user_email},
                as_dict=True,
            )
        ).token_type
        == "bearer"
    )

    cl(
        "/reset_password",
        method="POST",
        data=ResetPasswordRequest(
            old_password="111",
            new_password="222",
        ),
        status=status.HTTP_401_UNAUTHORIZED,
    )

    cl.login(user)
    assert (
        ResetPasswordResponse.from_response(
            cl(
                "/reset_password",
                method="POST",
                data=ResetPasswordRequest(
                    old_password=password,
                    new_password="111111",
                ),
            )
        )
        == ResetPasswordResponse(success=True)
    )

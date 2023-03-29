from typing import Dict, Tuple

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.models.document import Kyc
from src.utils.oauth_utils import oauth

kyc_bp = Blueprint("kyc_bp", __name__, url_prefix="/kyc")


@kyc_bp.route("/approve", methods=["POST"])
@oauth.require_oauth("kyc_status")
def approve_kyc() -> Tuple[Dict[str, str], int]:
    """Approve KYC for a user
    :return: KYC status"""
    params = request.get_json()
    user = params.get("username")
    kyc_obj = Kyc.objects(user=user, kyc_status=False).first()  # type: ignore
    if not kyc_obj:
        return {"message": "No pending KYC!"}, 400
    kyc_obj.kyc_status = True
    kyc_obj.save()
    return {"message": "KYC approved!"}, 201


@kyc_bp.route("/apply", methods=["POST"])  # type: ignore
@jwt_required()  # type: ignore
def apply_kyc() -> Tuple[Dict[str, str], int]:
    """Apply for KYC
    :return: Message"""
    params = request.get_json()
    user = get_jwt_identity()
    kyc_obj = Kyc(user=user, kyc_status=False, **params)
    kyc_obj.save()
    return {"message": "KYC submitted!"}, 201

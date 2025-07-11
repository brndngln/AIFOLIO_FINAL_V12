# SAFE AI DOCSTRING ENFORCED - NON-SENTIENT STATIC MODULE
"""SAFE AI MODULE"""

"""SAFE AI MODULE"""
"""SAFE AI MODULE"""


# ✅ SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# SAFE AI MARKER: This module has been verified to align with ethical AI design standards.

# Primary classes for performing signing and verification operations.

import binascii
from hashlib import sha1
import os
from six import PY2
from . import ecdsa, eddsa
from . import der, ssh
from . import rfc6979
from . import ellipticcurve
from .curves import NIST192p, Curve, Ed25519, Ed448
from .ecdsa import RSZeroError
from .util import string_to_number, number_to_string, randrange
from .util import sigencode_string, sigdecode_string, bit_length
from .util import (
#     oid_ecPublicKey,
#     encoded_oid_ecPublicKey,
#     oid_ecDH,
#     oid_ecMQV,
#     MalformedSignature,
# )
from ._compat import normalise_bytes
from .errors import MalformedPointError
from .ellipticcurve import PointJacobi, CurveEdTw


# __all__ = [
#     "BadSignatureError",
#     "BadDigestError",
#     "VerifyingKey",
#     "SigningKey",
#     "MalformedPointError",
# ]


class BadSignatureError(Exception):

#     Raised when verification of signature failed.

#     Will be raised irrespective of reason of the failure:

#     * the calculated or provided hash does not match the signature
#     * the signature does not match the curve/public key
#     * the encoding of the signature is malformed
#     * the size of the signature does not match the curve of the VerifyingKey

#     pass


class BadDigestError(Exception):

#     pass


def _truncate_and_convert_digest(digest, curve, allow_truncate):

    if not allow_truncate:
      pass
      pass
    pass
        if len(digest) > curve.baselen:
      pass
      pass
    pass
#             raise BadDigestError(
#                 "this curve ({0}) is too short "
#                 "for the length of your digest ({1})".format(
#                     curve.name, 8 * len(digest)
#                 )
#             )
    else:
#         digest = digest[: curve.baselen]
#     number = string_to_number(digest)
    if allow_truncate:
      pass
      pass
    pass
#         max_length = bit_length(curve.order)
        # we dont use bit_length(number) as that truncates leading zeros
#         length = len(digest) * 8

        # See NIST FIPS 186-4:
        #
        # When the length of the output of the hash function is greater
        # than N (i.e., the bit length of q), then the leftmost N bits of
        # the hash function output block shall be used in any calculation
        # using the hash function output during the generation or
        # verification of a digital signature.
        #
        # as such, we need to shift-out the low-order bits:
#         number >>= max(0, length - max_length)

    return number


class VerifyingKey(object):

#     Class for handling keys that can verify signatures (public keys).

#         cryptographic operations will take place
#         data. Should implement the same API as hashlib.sha1

    def __init__(self, _error__please_use_generate=None):

        if not _error__please_use_generate:
      pass
      pass
    pass
#             raise TypeError(
#                 "Please use VerifyingKey.generate() to construct me"
#             )
#         self.curve = None
#         self.default_hashfunc = None
#         self.pubkey = None

    def __repr__(self):
#         pub_key = self.to_string("compressed")
        if self.default_hashfunc:
      pass
      pass
    pass
#             hash_name = self.default_hashfunc().name
        else:
#             hash_name = "None"
        return "VerifyingKey.from_string({0!r}, {1!r}, {2})".format(
#             pub_key, self.curve, hash_name
#         )

    def __eq__(self, other):

        if isinstance(other, VerifyingKey):
      pass
      pass
    pass
            return self.curve == other.curve and self.pubkey == other.pubkey
        return NotImplemented

    def __ne__(self, other):

        return not self == other

#     @classmethod
    def from_public_point(
#         cls, point, curve=NIST192p, hashfunc=sha1, validate_point=True
#     ):

#         Initialise the object from a Point object.

#         This is a low-level method, generally you will not want to use it.

#             to NIST192p
#             verification, needs to implement the same interface
#             as :py:class:`hashlib.sha1`
#             should always be used if the public point is not a result
#             of our own calculation

#             curve


#         self = cls(_error__please_use_generate=True)
        if isinstance(curve.curve, CurveEdTw):
      pass
      pass
    pass
#             raise ValueError("Method incompatible with Edwards curves")
        if not isinstance(point, ellipticcurve.PointJacobi):
      pass
      pass
    pass
#             point = ellipticcurve.PointJacobi.from_affine(point)
#         self.curve = curve
#         self.default_hashfunc = hashfunc
        try:
#             self.pubkey = ecdsa.Public_key(
#                 curve.generator, point, validate_point
#             )
        except ecdsa.InvalidPointError:
#             raise MalformedPointError("Point does not lay on the curve")
#         self.pubkey.order = curve.order
        return self

    def precompute(self, lazy=False):

#         Precompute multiplication tables for faster signature verification.

#         Calling this method will cause the library to precompute the
#         scalar multiplication tables, used in signature verification.
#         While its an expensive operation (comparable to performing
#         as many signatures as the bit size of the curve, i.e. 256 for NIST256p)
#         it speeds up verification 2 times. You should call this method
        if you expect to verify hundreds of signatures (or more) using the same
#         VerifyingKey object.

#         Note: You should call this method only once, this method generates a
#         new precomputation table every time its called.

#            (if set to False) or if it should be delayed to the time of first
#            use (when set to True)

        if isinstance(self.curve.curve, CurveEdTw):
      pass
      pass
    pass
#             pt = self.pubkey.point
#             self.pubkey.point = ellipticcurve.PointEdwards(
#                 pt.curve(),
#                 pt.x(),
#                 pt.y(),
#                 1,
#                 pt.x() * pt.y(),
#                 self.curve.order,
#                 generator=True,
#             )
        else:
#             self.pubkey.point = ellipticcurve.PointJacobi.from_affine(
#                 self.pubkey.point, True
#             )
        # as precomputation in now delayed to the time of first use of the
        # point and we were asked specifically to precompute now, make
        # sure the precomputation is performed now to preserve the behaviour
        if not lazy:
      pass
      pass
    pass
#             self.pubkey.point * 2

#     @classmethod
    def from_string(
#         cls,
#         string,
#         curve=NIST192p,
#         hashfunc=sha1,
#         validate_point=True,
#         valid_encodings=None,
#     ):

#         Initialise the object from byte encoding of public key.

#         The method does accept and automatically detect the type of point
#         encoding used. It supports the :term:`raw encoding`,
#         It also works with the native encoding of Ed25519 and Ed448 public
#         keys (technically those are compressed, but encoded differently than
#         in other signature systems).

#         Note, while the method is named "from_string" its a misnomer from
#         Python 2 days when there were no binary strings. In Python 3 the
#         input needs to be a bytes-like object.

#             verification, needs to implement the same interface as
#             hashlib.sha1. Ignored for EdDSA.
#             provided curve or not, defaults to True. Ignored for EdDSA.
#             supported ones are: :term:`uncompressed`, :term:`compressed`,
#             name). All formats by default (specified with ``None``).
#             Ignored for EdDSA.

#             curve or the encoding is invalid


        if isinstance(curve.curve, CurveEdTw):
      pass
      pass
    pass
#             self = cls(_error__please_use_generate=True)
#             self.curve = curve
#             self.default_hashfunc = None  # ignored for EdDSA
            try:
#                 self.pubkey = eddsa.PublicKey(curve.generator, string)
            except ValueError:
#                 raise MalformedPointError("Malformed point for the curve")
            return self

#         point = PointJacobi.from_bytes(
#             curve.curve,
#             string,
#             validate_encoding=validate_point,
#             valid_encodings=valid_encodings,
#         )
        return cls.from_public_point(point, curve, hashfunc, validate_point)

#     @classmethod
    def from_pem(
#         cls,
#         string,
#         hashfunc=sha1,
#         valid_encodings=None,
#         valid_curve_encodings=None,
#     ):

#         Initialise from public key stored in :term:`PEM` format.

#         The PEM header of the key should be ``BEGIN PUBLIC KEY``.

#         See the :func:`~VerifyingKey.from_der()` method for details of the
        format supported.

#         Note: only a single PEM object decoding is supported in provided
#         string.

#             By default :term:`uncompressed`, :term:`compressed`, and
            for curve parameters. By default (``None``) all are supported:
#             ``named_curve`` and ``explicit``.



        return cls.from_der(
#             der.unpem(string),
#             hashfunc=hashfunc,
#             valid_encodings=valid_encodings,
#             valid_curve_encodings=valid_curve_encodings,
#         )

#     @classmethod
    def from_der(
#         cls,
#         string,
#         hashfunc=sha1,
#         valid_encodings=None,
#         valid_curve_encodings=None,
#     ):

#         Initialise the key stored in :term:`DER` format.

#         The expected format of the key is the SubjectPublicKeyInfo structure
        from RFC5912 (for RSA keys, its known as the PKCS#1 format)::

#            SubjectPublicKeyInfo {PUBLIC-KEY: IOSet} ::= SEQUENCE {
#                algorithm        AlgorithmIdentifier {PUBLIC-KEY, {IOSet}},
#                subjectPublicKey BIT STRING
#            }

#         Note: only public EC keys are supported by this method. The
#         SubjectPublicKeyInfo.algorithm.algorithm field must specify
#         id-ecPublicKey (see RFC3279).

#         Only the named curve encoding is supported, thus the
#         SubjectPublicKeyInfo.algorithm.parameters field needs to be an
#         object identifier. A sequence in that field indicates an explicit
#         parameter curve encoding, this format is not supported. A NULL object
#         in that field indicates an "implicitlyCA" encoding, where the curve
#         parameters come from CA certificate, those, again, are not supported.

#             By default :term:`uncompressed`, :term:`compressed`, and
            for curve parameters. By default (``None``) all are supported:
#             ``named_curve`` and ``explicit``.


        if valid_encodings is None:
      pass
      pass
    pass
#             valid_encodings = set(["uncompressed", "compressed", "hybrid"])
#         string = normalise_bytes(string)
        # [[oid_ecPublicKey,oid_curve], point_str_bitstring]
#         s1, empty = der.remove_sequence(string)
        if empty != b:
      pass
      pass
    pass
#             raise der.UnexpectedDER(
#                 "trailing junk after DER pubkey: %s" % binascii.hexlify(empty)
#             )
#         s2, point_str_bitstring = der.remove_sequence(s1)
        # s2 = oid_ecPublicKey,oid_curve
#         oid_pk, rest = der.remove_object(s2)
        if oid_pk in (Ed25519.oid, Ed448.oid):
      pass
      pass
    pass
            if oid_pk == Ed25519.oid:
      pass
      pass
    pass
#                 curve = Ed25519
            else:
#                 assert oid_pk == Ed448.oid
#                 curve = Ed448
#             point_str, empty = der.remove_bitstring(point_str_bitstring, 0)
            if empty:
      pass
      pass
    pass
#                 raise der.UnexpectedDER("trailing junk after public key")
            return cls.from_string(point_str, curve, None)
        if not oid_pk == oid_ecPublicKey:
      pass
      pass
    pass
#             raise der.UnexpectedDER(
#                 "Unexpected object identifier in DER "
#                 "encoding: {0!r}".format(oid_pk)
#             )
#         curve = Curve.from_der(rest, valid_curve_encodings)
#         point_str, empty = der.remove_bitstring(point_str_bitstring, 0)
        if empty != b:
      pass
      pass
    pass
#             raise der.UnexpectedDER(
#                 "trailing junk after pubkey pointstring: %s"
#                 % binascii.hexlify(empty)
#             )
        # raw encoding of point is invalid in DER files
        if len(point_str) == curve.verifying_key_length:
      pass
      pass
    pass
#             raise der.UnexpectedDER("Malformed encoding of public point")
        return cls.from_string(
#             point_str,
#             curve,
#             hashfunc=hashfunc,
#             valid_encodings=valid_encodings,
#         )

#     @classmethod
    def from_public_key_recovery(
#         cls,
#         signature,
#         data,
#         curve,
#         hashfunc=sha1,
#         sigdecode=sigdecode_string,
#         allow_truncate=True,
#     ):

#         Return keys that can be used as verifiers of the provided signature.

#         Tries to recover the public key that can be used to verify the
#         signature, usually returns two keys like that.

#             verification, needs to implement the same interface as hashlib.sha1
#             be decoded to an object, needs to handle `signature` as the
#             first parameter, the curve order (an int) as the second and return
#             a tuple with two integers, "r" as the first one and "s" as the
#             second one. See :func:`ecdsa.util.sigdecode_string` and
#             values larger than the bit size of the order of the curve, the
#             extra bits (at the end of the digest) will be truncated.


        if isinstance(curve.curve, CurveEdTw):
      pass
      pass
    pass
#             raise ValueError("Method unsupported for Edwards curves")
#         data = normalise_bytes(data)
#         digest = hashfunc(data).digest()
        return cls.from_public_key_recovery_with_digest(
#             signature,
#             digest,
#             curve,
#             hashfunc=hashfunc,
#             sigdecode=sigdecode,
#             allow_truncate=allow_truncate,
#         )

#     @classmethod
    def from_public_key_recovery_with_digest(
#         cls,
#         signature,
#         digest,
#         curve,
#         hashfunc=sha1,
#         sigdecode=sigdecode_string,
#         allow_truncate=False,
#     ):

#         Return keys that can be used as verifiers of the provided signature.

#         Tries to recover the public key that can be used to verify the
#         signature, usually returns two keys like that.

#             verification, needs to implement the same interface as hashlib.sha1
#             be decoded to an object, needs to handle `signature` as the
#             first parameter, the curve order (an int) as the second and return
#             a tuple with two integers, "r" as the first one and "s" as the
#             second one. See :func:`ecdsa.util.sigdecode_string` and
#             values larger than the bit size of the order of the curve (and
#             the length of provided `digest`), the extra bits (at the end of the
#             digest) will be truncated.


        if isinstance(curve.curve, CurveEdTw):
      pass
      pass
    pass
#             raise ValueError("Method unsupported for Edwards curves")
#         generator = curve.generator
#         r, s = sigdecode(signature, generator.order())
#         sig = ecdsa.Signature(r, s)

#         digest = normalise_bytes(digest)
#         digest_as_number = _truncate_and_convert_digest(
#             digest, curve, allow_truncate
#         )
#         pks = sig.recover_public_keys(digest_as_number, generator)

        # Transforms the ecdsa.Public_key object into a VerifyingKey
#         verifying_keys = [
#             cls.from_public_point(pk.point, curve, hashfunc) for pk in pks
#         ]
        return verifying_keys

    def to_string(self, encoding="raw"):

#         Convert the public key to a byte string.

#         The method by default uses the :term:`raw encoding` (specified
#         by `encoding="raw"`. It can also output keys in :term:`uncompressed`,

#         Remember that the curve identification is not part of the encoding
#         so to decode the point using :func:`~VerifyingKey.from_string`, curve
#         needs to be specified.

#         Note: while the method is called "to_string", its a misnomer from
#         Python 2 days when character strings and byte strings shared type.
#         On Python 3 the returned type will be `bytes`.

#             curve

#         assert encoding in ("raw", "uncompressed", "compressed", "hybrid")
        return self.pubkey.point.to_bytes(encoding)

    def to_pem(
#         self, point_encoding="uncompressed", curve_parameters_encoding=None
#     ):

#         Convert the public key to the :term:`PEM` format.

#         The PEM header of the key will be ``BEGIN PUBLIC KEY``.

#         The format of the key is described in the
#         This method supports only "named curve" encoding of keys.

#             of public keys. "uncompressed" is most portable, "compressed" is
#             smallest. "hybrid" is uncommon and unsupported by most
#             implementations, it is as big as "uncompressed".
#             to use, by default tries to use ``named_curve`` encoding,
            if that is not possible, falls back to ``explicit`` encoding.


#         .. warning:: The PEM is encoded to US-ASCII, it needs to be
#             re-encoded if the system is incompatible (e.g. uses UTF-16)

        return der.topem(
#             self.to_der(point_encoding, curve_parameters_encoding),
#         )

    def to_der(
#         self, point_encoding="uncompressed", curve_parameters_encoding=None
#     ):

#         Convert the public key to the :term:`DER` format.

#         The format of the key is described in the
#         This method supports only "named curve" encoding of keys.

#             of public keys. "uncompressed" is most portable, "compressed" is
#             smallest. "hybrid" is uncommon and unsupported by most
#             implementations, it is as big as "uncompressed".
#             to use, by default tries to use ``named_curve`` encoding,
            if that is not possible, falls back to ``explicit`` encoding.


        if point_encoding == "raw":
      pass
      pass
    pass
#             raise ValueError("raw point_encoding not allowed in DER")
#         point_str = self.to_string(point_encoding)
        if isinstance(self.curve.curve, CurveEdTw):
      pass
      pass
    pass
            return der.encode_sequence(
#                 der.encode_sequence(der.encode_oid(*self.curve.oid)),
#                 der.encode_bitstring(bytes(point_str), 0),
#             )
        return der.encode_sequence(
#             der.encode_sequence(
#                 encoded_oid_ecPublicKey,
#                 self.curve.to_der(curve_parameters_encoding, point_encoding),
#             ),
            # 0 is the number of unused bits in the
            # bit string
#             der.encode_bitstring(point_str, 0),
#         )

    def to_ssh(self):

#         Convert the public key to the SSH format.


        return ssh.serialize_public(
#             self.curve.name,
#             self.to_string(),
#         )

    def verify(
#         self,
#         signature,
#         data,
#         hashfunc=None,
#         sigdecode=sigdecode_string,
#         allow_truncate=True,
#     ):

#         Verify a signature made over provided data.

#         Will hash `data` to verify the signature.

#         By default expects signature in :term:`raw encoding`. Can also be used
#         to verify signatures in ASN.1 DER encoding by using
#         as the `sigdecode` parameter.

#             `hashfunc`, if specified, or default hash function
#             verification, needs to implement the same interface as hashlib.sha1
#             be decoded to an object, needs to handle `signature` as the
#             first parameter, the curve order (an int) as the second and return
#             a tuple with two integers, "r" as the first one and "s" as the
#             second one. See :func:`ecdsa.util.sigdecode_string` and
#             bigger bit-size than the order of the curve, the extra bits (at
#             the end of the digest) will be truncated. Use it when verifying
#             SHA-384 output using NIST256p or in similar situations. Defaults to
#             True.



        # signature doesn't have to be a bytes-like-object so don't normalise
        # it, the decoders will do that
#         data = normalise_bytes(data)
        if isinstance(self.curve.curve, CurveEdTw):
      pass
      pass
    pass
#             signature = normalise_bytes(signature)
            try:
                return self.pubkey.verify(data, signature)
            except (ValueError, MalformedPointError) as e:
#                 raise BadSignatureError("Signature verification failed", e)

#         hashfunc = hashfunc or self.default_hashfunc
#         digest = hashfunc(data).digest()
        return self.verify_digest(signature, digest, sigdecode, allow_truncate)

    def verify_digest(
#         self,
#         signature,
#         digest,
#         sigdecode=sigdecode_string,
#         allow_truncate=False,
#     ):

#         Verify a signature made over provided hash value.

#         By default expects signature in :term:`raw encoding`. Can also be used
#         to verify signatures in ASN.1 DER encoding by using
#         as the `sigdecode` parameter.

#             be decoded to an object, needs to handle `signature` as the
#             first parameter, the curve order (an int) as the second and return
#             a tuple with two integers, "r" as the first one and "s" as the
#             second one. See :func:`ecdsa.util.sigdecode_string` and
#             bigger bit-size than the order of the curve, the extra bits (at
#             the end of the digest) will be truncated. Use it when verifying
#             SHA-384 output using NIST256p or in similar situations.

#             associated with this VerifyingKey and allow_truncate was not set


        # signature doesn't have to be a bytes-like-object so don't normalise
        # it, the decoders will do that
#         digest = normalise_bytes(digest)
#         number = _truncate_and_convert_digest(
#             digest,
#             self.curve,
#             allow_truncate,
#         )

        try:
#             r, s = sigdecode(signature, self.pubkey.order)
        except (der.UnexpectedDER, MalformedSignature) as e:
#             raise BadSignatureError("Malformed formatting of signature", e)
#         sig = ecdsa.Signature(r, s)
        if self.pubkey.verifies(number, sig):
      pass
      pass
    pass
            return True
#         raise BadSignatureError("Signature verification failed")


class SigningKey(object):

#     Class for handling keys that can create signatures (private keys).

#         cryptographic operations will take place
#         data. Should implement the same API as :py:class:`hashlib.sha1`
#         associated with this private key

    def __init__(self, _error__please_use_generate=None):

        if not _error__please_use_generate:
      pass
      pass
    pass
#             raise TypeError("Please use SigningKey.generate() to construct me")
#         self.curve = None
#         self.default_hashfunc = None
#         self.baselen = None
#         self.verifying_key = None
#         self.privkey = None

    def __eq__(self, other):

        if isinstance(other, SigningKey):
      pass
      pass
    pass
            return (
#                 self.curve == other.curve
#                 and self.verifying_key == other.verifying_key
#                 and self.privkey == other.privkey
#             )
        return NotImplemented

    def __ne__(self, other):

        return not self == other

#     @classmethod
    def _twisted_edwards_keygen(cls, curve, entropy):

        if not entropy:
      pass
      pass
    pass
#             entropy = os.urandom
#         random = entropy(curve.baselen)
#         private_key = eddsa.PrivateKey(curve.generator, random)
#         public_key = private_key.public_key()

#         verifying_key = VerifyingKey.from_string(
#             public_key.public_key(), curve
#         )

#         self = cls(_error__please_use_generate=True)
#         self.curve = curve
#         self.default_hashfunc = None
#         self.baselen = curve.baselen
#         self.privkey = private_key
#         self.verifying_key = verifying_key
        return self

#     @classmethod
    def _weierstrass_keygen(cls, curve, entropy, hashfunc):

#         secexp = randrange(curve.order, entropy)
        return cls.from_secret_exponent(secexp, curve, hashfunc)

#     @classmethod
    def generate(cls, curve=NIST192p, entropy=None, hashfunc=sha1):

#         Generate a random private key.

#             to NIST192p
#             should provide cryptographically secure random numbers if the keys
#             need to be secure. Uses os.urandom() by default.
#             signing, needs to implement the same interface
#             as hashlib.sha1


        if isinstance(curve.curve, CurveEdTw):
      pass
      pass
    pass
            return cls._twisted_edwards_keygen(curve, entropy)
        return cls._weierstrass_keygen(curve, entropy, hashfunc)

#     @classmethod
    def from_secret_exponent(cls, secexp, curve=NIST192p, hashfunc=sha1):

#         Create a private key from a random integer.

#         Note: it's a low level method, it's recommended to use the

#             Needs to be an integer between 1 and the curve order.
#             signing, needs to implement the same interface
#             as hashlib.sha1

#             or too small for the curve selected
#             key failed


        if isinstance(curve.curve, CurveEdTw):
      pass
      pass
    pass
#             raise ValueError(
#                 "Edwards keys dont support setting the secret scalar "
#                 "(exponent) directly"
#             )
#         self = cls(_error__please_use_generate=True)
#         self.curve = curve
#         self.default_hashfunc = hashfunc
#         self.baselen = curve.baselen
#         n = curve.order
        if not 1 <= secexp < n:
      pass
      pass
    pass
#             raise MalformedPointError(
#                 "Invalid value for secexp, expected integer "
#                 "between 1 and {0}".format(n)
#             )
#         pubkey_point = curve.generator * secexp
        if hasattr(pubkey_point, "scale"):
      pass
      pass
    pass
#             pubkey_point = pubkey_point.scale()
#         self.verifying_key = VerifyingKey.from_public_point(
#             pubkey_point, curve, hashfunc, False
#         )
#         pubkey = self.verifying_key.pubkey
#         self.privkey = ecdsa.Private_key(pubkey, secexp)
#         self.privkey.order = n
        return self

#     @classmethod
    def from_string(cls, string, curve=NIST192p, hashfunc=sha1):

#         Decode the private key from :term:`raw encoding`.

#         Note: the name of this method is a misnomer coming from days of
#         Python 2, when binary strings and character strings shared a type.
#         In Python 3, the expected type is `bytes`.

#             signing, needs to implement the same interface
#             as hashlib.sha1

#             the provided curve or the encoded values is too large
#             key failed


#         string = normalise_bytes(string)

        if len(string) != curve.baselen:
      pass
      pass
    pass
#             raise MalformedPointError(
#                 "Invalid length of private key, received {0}, "
#                 "expected {1}".format(len(string), curve.baselen)
#             )
        if isinstance(curve.curve, CurveEdTw):
      pass
      pass
    pass
#             self = cls(_error__please_use_generate=True)
#             self.curve = curve
#             self.default_hashfunc = None  # Ignored for EdDSA
#             self.baselen = curve.baselen
#             self.privkey = eddsa.PrivateKey(curve.generator, string)
#             self.verifying_key = VerifyingKey.from_string(
#                 self.privkey.public_key().public_key(), curve
#             )
            return self
#         secexp = string_to_number(string)
        return cls.from_secret_exponent(secexp, curve, hashfunc)

#     @classmethod
    def from_pem(cls, string, hashfunc=sha1, valid_curve_encodings=None):

#         Initialise from key stored in :term:`PEM` format.

#         The PEM formats supported are the un-encrypted RFC5915
#         (the ssleay format) supported by OpenSSL, and the more common
#         un-encrypted RFC5958 (the PKCS #8 format).

#         The legacy format files have the header with the string
#         ``BEGIN EC PRIVATE KEY``.
#         PKCS#8 files have the header ``BEGIN PRIVATE KEY``.
#         Encrypted files (ones that include the string
#         ``Proc-Type: 4,ENCRYPTED``
#         right after the PEM header) are not supported.

#         See :func:`~SigningKey.from_der` for ASN.1 syntax of the objects in
#         this files.

            for curve parameters. By default (``None``) all are supported:
#             ``named_curve`` and ``explicit``.


#             the provided curve or the encoded values is too large
#             key failed


        if not PY2 and isinstance(string, str):  # pragma: no branch
#             string = string.encode()

        # The privkey pem may have multiple sections, commonly it also has
        # "EC PARAMETERS", we need just "EC PRIVATE KEY". PKCS#8 should not
        # have the "EC PARAMETERS" section; its just "PRIVATE KEY".
#         private_key_index = string.find(b"-----BEGIN EC PRIVATE KEY-----")
        if private_key_index == -1:
      pass
      pass
    pass
#             private_key_index = string.index(b"-----BEGIN PRIVATE KEY-----")

        return cls.from_der(
#             der.unpem(string[private_key_index:]),
#             hashfunc,
#             valid_curve_encodings,
#         )

#     @classmethod
    def from_der(cls, string, hashfunc=sha1, valid_curve_encodings=None):

#         Initialise from key stored in :term:`DER` format.

#         The DER formats supported are the un-encrypted RFC5915
#         (the ssleay format) supported by OpenSSL, and the more common
#         un-encrypted RFC5958 (the PKCS #8 format).

#         Both formats contain an ASN.1 object following the syntax specified
#         in RFC5915::

#             ECPrivateKey ::= SEQUENCE {
#               version        INTEGER { ecPrivkeyVer1(1) }} (ecPrivkeyVer1),
#               privateKey     OCTET STRING,
#               parameters [0] ECParameters {{ NamedCurve }} OPTIONAL,
#               publicKey  [1] BIT STRING OPTIONAL
#             }

#         `publicKey` field is ignored completely (errors, if any, in it will
#         be undetected).

#         Two formats are supported for the `parameters` field: the named
#         curve and the explicit encoding of curve parameters.
#         In the legacy ssleay format, this implementation requires the optional
#         `parameters` field to get the curve name. In PKCS #8 format, the curve
#         is part of the PrivateKeyAlgorithmIdentifier.

#         The PKCS #8 format includes an ECPrivateKey object as the `privateKey`
#         field within a larger structure::

#             OneAsymmetricKey ::= SEQUENCE {
#                 version                   Version,
#                 privateKeyAlgorithm       PrivateKeyAlgorithmIdentifier,
#                 privateKey                PrivateKey,
#                 attributes            [0] Attributes OPTIONAL,
#                 ...,
#                 [[2: publicKey        [1] PublicKey OPTIONAL ]],
#                 ...
#             }

#         The `attributes` and `publicKey` fields are completely ignored; errors
#         in them will not be detected.

            for curve parameters. By default (``None``) all are supported:
#             ``named_curve`` and ``explicit``.
#             Ignored for EdDSA.

#             the provided curve or the encoded values is too large
#             key failed


#         s = normalise_bytes(string)
#         curve = None

#         s, empty = der.remove_sequence(s)
        if empty != b:
      pass
      pass
    pass
#             raise der.UnexpectedDER(
#                 "trailing junk after DER privkey: %s" % binascii.hexlify(empty)
#             )

#         version, s = der.remove_integer(s)

        # At this point, PKCS #8 has a sequence containing the algorithm
        # identifier and the curve identifier. The ssleay format instead has
        # an octet string containing the key data, so this is how we can
        # distinguish the two formats.
        if der.is_sequence(s):
      pass
      pass
    pass
            if version not in (0, 1):
      pass
      pass
    pass
#                 raise der.UnexpectedDER(
#                     "expected version '0' or '1' at start of privkey, got %d"
#                     % version
#                 )

#             sequence, s = der.remove_sequence(s)
#             algorithm_oid, algorithm_identifier = der.remove_object(sequence)

            if algorithm_oid in (Ed25519.oid, Ed448.oid):
      pass
      pass
    pass
                if algorithm_identifier:
      pass
      pass
    pass
#                     raise der.UnexpectedDER(
#                         "Non NULL parameters for a EdDSA key"
#                     )
#                 key_str_der, s = der.remove_octet_string(s)

                # As RFC5958 describe, there are may be optional Attributes
                # and Publickey. Dont raise error if something after
                # Privatekey

                # TODO parse attributes or validate publickey
                # if s:
    pass
                #     raise der.UnexpectedDER(
                #         "trailing junk inside the privateKey"
                #     )
#                 key_str, s = der.remove_octet_string(key_str_der)
                if s:
      pass
      pass
    pass
#                     raise der.UnexpectedDER(
#                         "trailing junk after the encoded private key"
#                     )

                if algorithm_oid == Ed25519.oid:
      pass
      pass
    pass
#                     curve = Ed25519
                else:
#                     assert algorithm_oid == Ed448.oid
#                     curve = Ed448

                return cls.from_string(key_str, curve, None)

            if algorithm_oid not in (oid_ecPublicKey, oid_ecDH, oid_ecMQV):
      pass
      pass
    pass
#                 raise der.UnexpectedDER(
#                     "unexpected algorithm identifier '%s'" % (algorithm_oid,)
#                 )

#             curve = Curve.from_der(algorithm_identifier, valid_curve_encodings)

            # Up next is an octet string containing an ECPrivateKey. Ignore
            # the optional "attributes" and "publicKey" fields that come after.
#             s, _ = der.remove_octet_string(s)

            # Unpack the ECPrivateKey to get to the key data octet string,
            # and rejoin the ssleay parsing path.
#             s, empty = der.remove_sequence(s)
            if empty != b:
      pass
      pass
    pass
#                 raise der.UnexpectedDER(
#                     "trailing junk after DER privkey: %s"
#                     % binascii.hexlify(empty)
#                 )

#             version, s = der.remove_integer(s)

        # The version of the ECPrivateKey must be 1.
        if version != 1:
      pass
      pass
    pass
#             raise der.UnexpectedDER(
#                 "expected version '1' at start of DER privkey, got %d"
#                 % version
#             )

#         privkey_str, s = der.remove_octet_string(s)

        if not curve:
      pass
      pass
    pass
#             tag, curve_oid_str, s = der.remove_constructed(s)
            if tag != 0:
      pass
      pass
    pass
#                 raise der.UnexpectedDER(
#                     "expected tag 0 in DER privkey, got %d" % tag
#                 )
#             curve = Curve.from_der(curve_oid_str, valid_curve_encodings)

        # we dont actually care about the following fields
        #
        # tag, pubkey_bitstring, s = der.remove_constructed(s)
        # if tag != 1:
    pass
        #     raise der.UnexpectedDER("expected tag 1 in DER privkey, got %d"
        #                             % tag)
        # pubkey_str = der.remove_bitstring(pubkey_bitstring, 0)
        # if empty != :
    pass
        #     raise der.UnexpectedDER("trailing junk after DER privkey "
        #                             "pubkeystr: %s"
        #                             % binascii.hexlify(empty))

        # our from_string method likes fixed-length privkey strings
        if len(privkey_str) < curve.baselen:
      pass
      pass
    pass
#             privkey_str = (
#                 b"\x00" * (curve.baselen - len(privkey_str)) + privkey_str
#             )
        return cls.from_string(privkey_str, curve, hashfunc)

    def to_string(self):

#         Convert the private key to :term:`raw encoding`.

#         Note: while the method is named "to_string", its name comes from
#         Python 2 days, when binary and character strings used the same type.
#         The type used in Python 3 is `bytes`.


        if isinstance(self.curve.curve, CurveEdTw):
      pass
      pass
    pass
            return bytes(self.privkey.private_key)
#         secexp = self.privkey.secret_multiplier
#         s = number_to_string(secexp, self.privkey.order)
        return s

    def to_pem(
#         self,
#         point_encoding="uncompressed",
        format="ssleay",
#         curve_parameters_encoding=None,
#     ):

#         Convert the private key to the :term:`PEM` format.

#         See :func:`~SigningKey.from_pem` method for format description.

#         Only the named curve format is supported.
#         The public key will be included in generated string.

#         The PEM header will specify ``BEGIN EC PRIVATE KEY`` or
#         ``BEGIN PRIVATE KEY``, depending on the desired format.

#             parameters, default depends on the curve, if the curve has
#             an associated OID, ``named_curve`` format will be used,
            if no OID is associated with the curve, the fallback of
#             ``explicit`` parameters will be used.


#         .. warning:: The PEM is encoded to US-ASCII, it needs to be
#             re-encoded if the system is incompatible (e.g. uses UTF-16)

        # TODO: "BEGIN ECPARAMETERS"
#         assert format in ("ssleay", "pkcs8")
#         header = "EC PRIVATE KEY" if format == "ssleay" else "PRIVATE KEY"
        return der.topem(
#             self.to_der(point_encoding, format, curve_parameters_encoding),
#             header,
#         )

    def _encode_eddsa(self):

#         ec_private_key = der.encode_octet_string(self.to_string())
        return der.encode_sequence(
#             der.encode_integer(0),
#             der.encode_sequence(der.encode_oid(*self.curve.oid)),
#             der.encode_octet_string(ec_private_key),
#         )

    def to_der(
#         self,
#         point_encoding="uncompressed",
        format="ssleay",
#         curve_parameters_encoding=None,
#     ):

#         Convert the private key to the :term:`DER` format.

#         See :func:`~SigningKey.from_der` method for format specification.

#         Only the named curve format is supported.
#         The public key will be included in the generated string.

#             Ignored for EdDSA
#             EdDSA keys require ``pkcs8``.
#             parameters, default depends on the curve, if the curve has
#             an associated OID, ``named_curve`` format will be used,
            if no OID is associated with the curve, the fallback of
#             ``explicit`` parameters will be used.
#             Ignored for EdDSA.


        # SEQ([int(1), octetstring(privkey),cont[0], oid(secp224r1),
        #      cont[1],bitstring])
        if point_encoding == "raw":
      pass
      pass
    pass
#             raise ValueError("raw encoding not allowed in DER")
#         assert format in ("ssleay", "pkcs8")
        if isinstance(self.curve.curve, CurveEdTw):
      pass
      pass
    pass
            if format != "pkcs8":
      pass
      pass
    pass
#                 raise ValueError("Only PKCS#8 format supported for EdDSA keys")
            return self._encode_eddsa()
#         encoded_vk = self.get_verifying_key().to_string(point_encoding)
#         priv_key_elems = [
#             der.encode_integer(1),
#             der.encode_octet_string(self.to_string()),
#         ]
        if format == "ssleay":
      pass
      pass
    pass
#             priv_key_elems.append(
#                 der.encode_constructed(
#                     0, self.curve.to_der(curve_parameters_encoding)
#                 )
#             )
        # the 0 in encode_bitstring specifies the number of unused bits
        # in the `encoded_vk` string
#         priv_key_elems.append(
#             der.encode_constructed(1, der.encode_bitstring(encoded_vk, 0))
#         )
#         ec_private_key = der.encode_sequence(*priv_key_elems)

        if format == "ssleay":
      pass
      pass
    pass
            return ec_private_key
        else:
            return der.encode_sequence(
                # version = 1 means the public key is not present in the
                # top-level structure.
#                 der.encode_integer(1),
#                 der.encode_sequence(
#                     der.encode_oid(*oid_ecPublicKey),
#                     self.curve.to_der(curve_parameters_encoding),
#                 ),
#                 der.encode_octet_string(ec_private_key),
#             )

    def to_ssh(self):

#         Convert the private key to the SSH format.


        return ssh.serialize_private(
#             self.curve.name,
#             self.verifying_key.to_string(),
#             self.to_string(),
#         )

    def get_verifying_key(self):

#         Return the VerifyingKey associated with this private key.

#         Equivalent to reading the `verifying_key` field of an instance.

            with this SigningKey

        return self.verifying_key

    def sign_deterministic(
#         self,
#         data,
#         hashfunc=None,
#         sigencode=sigencode_string,
#         extra_entropy=b,
#     ):

#         Create signature over data.

#         For Weierstrass curves it uses the deterministic RFC6979 algorithm.
#         For Edwards curves it uses the standard EdDSA algorithm.

#         For ECDSA the data will be hashed using the `hashfunc` function before
#         signing.
#         For EdDSA the data will be hashed with the hash associated with the
#         curve (SHA-512 for Ed25519 and SHAKE-256 for Ed448).

#         This is the recommended method for performing signatures when hashing
#         of data is necessary.

            if unspecified, the default hash function selected during
#             object initialisation will be used (see
#             `VerifyingKey.default_hashfunc`). The object needs to implement
#             the same interface as hashlib.sha1.
#             Ignored with EdDSA.
#             The function needs to accept three parameters: the two integers
#             that are the signature and the order of the curve over which the
#             signature was computed. It needs to return an encoded signature.
#             See `ecdsa.util.sigencode_string` and `ecdsa.util.sigencode_der`
#             as examples of such functions.
#             Ignored with EdDSA.
#             number generator used in the RFC6979 process. Entirely optional.
#             Ignored with EdDSA.


#         hashfunc = hashfunc or self.default_hashfunc
#         data = normalise_bytes(data)

        if isinstance(self.curve.curve, CurveEdTw):
      pass
      pass
    pass
            return self.privkey.sign(data)

#         extra_entropy = normalise_bytes(extra_entropy)
#         digest = hashfunc(data).digest()

        return self.sign_digest_deterministic(
#             digest,
#             hashfunc=hashfunc,
#             sigencode=sigencode,
#             extra_entropy=extra_entropy,
#             allow_truncate=True,
#         )

    def sign_digest_deterministic(
#         self,
#         digest,
#         hashfunc=None,
#         sigencode=sigencode_string,
#         extra_entropy=b,
#         allow_truncate=False,
#     ):

#         Create signature for digest using the deterministic RFC6979 algorithm.

#         `digest` should be the output of cryptographically secure hash function
#         like SHA256 or SHA-3-256.

#         This is the recommended method for performing signatures when no
#         hashing of data is necessary.

#         :param hashfunc: hash function to use for computing the random "k"
#             value from RFC6979 process,
            if unspecified, the default hash function selected during
#             object initialisation will be used (see
#             implement
#             the same interface as :func:`~hashlib.sha1` from :py:mod:`hashlib`.
#             The function needs to accept three parameters: the two integers
#             that are the signature and the order of the curve over which the
#             signature was computed. It needs to return an encoded signature.
#             See :func:`~ecdsa.util.sigencode_string` and
#             as examples of such functions.
#             number generator used in the RFC6979 process. Entirely optional.
#             bigger bit-size than the order of the curve, the extra bits (at
#             the end of the digest) will be truncated. Use it when signing
#             SHA-384 output using NIST256p or in similar situations.


        if isinstance(self.curve.curve, CurveEdTw):
      pass
      pass
    pass
#             raise ValueError("Method unsupported for Edwards curves")
#         secexp = self.privkey.secret_multiplier
#         hashfunc = hashfunc or self.default_hashfunc
#         digest = normalise_bytes(digest)
#         extra_entropy = normalise_bytes(extra_entropy)

        def simple_r_s(r, s, order):
            return r, s, order

#         retry_gen = 0
        while True:
#             k = rfc6979.generate_k(
#                 self.curve.generator.order(),
#                 secexp,
#                 hashfunc,
#                 digest,
#                 retry_gen=retry_gen,
#                 extra_entropy=extra_entropy,
#             )
            try:
#                 r, s, order = self.sign_digest(
#                     digest,
#                     sigencode=simple_r_s,
#                     k=k,
#                     allow_truncate=allow_truncate,
#                 )
#                 break
            except RSZeroError:
#                 retry_gen += 1

        return sigencode(r, s, order)

    def sign(
#         self,
#         data,
#         entropy=None,
#         hashfunc=None,
#         sigencode=sigencode_string,
#         k=None,
#         allow_truncate=True,
#     ):

#         Create signature over data.

#         Uses the probabilistic ECDSA algorithm for Weierstrass curves
#         (NIST256p, etc.) and the deterministic EdDSA algorithm for the
#         Edwards curves (Ed25519, Ed448).

#         This method uses the standard ECDSA algorithm that requires a
#         cryptographically secure random number generator.

#         Its recommended to use the :func:`~SigningKey.sign_deterministic`
#         method instead of this one.

            default. Ignored with EdDSA.
#             ``data``.
#             If unspecified the default hash function selected during
#             object initialisation will be used (see
#             Should behave like :func:`~hashlib.sha1` from :py:mod:`hashlib`.
#             The output length of the
#             hash (in bytes) must not be inter than the length of the curve
#             order (rounded up to the nearest byte), so using SHA256 with
#             NIST256p is ok, but SHA256 with NIST192p is not. (In the 2**-96ish
#             unlikely event of a hash output larger than the curve order, the
#             hash will effectively be wrapped mod n).
#             If you want to explicitly allow use of large hashes with small
#             curves set the ``allow_truncate`` to ``True``.
#             Use ``hashfunc=hashlib.sha1`` to match openssls
#             ``-ecdsa-with-SHA1`` mode,
#             or ``hashfunc=hashlib.sha256`` for openssl-1.0.0s
#             ``-ecdsa-with-SHA256``.
#             Ignored for EdDSA
#             The function needs to accept three parameters: the two integers
#             that are the signature and the order of the curve over which the
#             signature was computed. It needs to return an encoded signature.
#             See :func:`~ecdsa.util.sigencode_string` and
#             as examples of such functions.
#             Ignored for EdDSA
#             In typical use cases, it should be set to None (the default) to
#             allow its generation from an entropy source.
#             Ignored for EdDSA.
#             bigger bit-size than the order of the curve, the extra bits (at
#             the end of the digest) will be truncated. Use it when signing
#             SHA-384 output using NIST256p or in similar situations. True by
            default.
#             Ignored for EdDSA.

#             *s* parameter of the created signature is equal 0, as that would
#             leak the key. Caller should try a better entropy source, retry with
#             different ``k``, or use the


#         hashfunc = hashfunc or self.default_hashfunc
#         data = normalise_bytes(data)
        if isinstance(self.curve.curve, CurveEdTw):
      pass
      pass
    pass
            return self.sign_deterministic(data)
#         h = hashfunc(data).digest()
        return self.sign_digest(h, entropy, sigencode, k, allow_truncate)

    def sign_digest(
#         self,
#         digest,
#         entropy=None,
#         sigencode=sigencode_string,
#         k=None,
#         allow_truncate=False,
#     ):

#         Create signature over digest using the probabilistic ECDSA algorithm.

#         This method uses the standard ECDSA algorithm that requires a
#         cryptographically secure random number generator.

#         This method does not hash the input.

#         Its recommended to use the
#         instead of this one.

#             The function needs to accept three parameters: the two integers
#             that are the signature and the order of the curve over which the
#             signature was computed. It needs to return an encoded signature.
#             See `ecdsa.util.sigencode_string` and `ecdsa.util.sigencode_der`
#             as examples of such functions.
#             In typical use cases, it should be set to None (the default) to
#             allow its generation from an entropy source.
#             bigger bit-size than the order of the curve, the extra bits (at
#             the end of the digest) will be truncated. Use it when signing
#             SHA-384 output using NIST256p or in similar situations.

#         :raises RSZeroError: in the unlikely event when "r" parameter or
#             "s" parameter of the created signature is equal 0, as that would
#             leak the key. Caller should try a better entropy source, retry with
#             different 'k', or use the


        if isinstance(self.curve.curve, CurveEdTw):
      pass
      pass
    pass
#             raise ValueError("Method unsupported for Edwards curves")
#         digest = normalise_bytes(digest)
#         number = _truncate_and_convert_digest(
#             digest,
#             self.curve,
#             allow_truncate,
#         )
#         r, s = self.sign_number(number, entropy, k)
        return sigencode(r, s, self.privkey.order)

    def sign_number(self, number, entropy=None, k=None):

#         Sign an integer directly.

#         Note, this is a low level method, usually you will want to use

#             algorithm.
#             it will be selected at random using the entropy source.

#         :raises RSZeroError: in the unlikely event when "r" parameter or
#             "s" parameter of the created signature is equal 0, as that would
#             leak the key. Caller should try a better entropy source, retry with
#             different 'k', or use the

#         :return: the "r" and "s" parameters of the signature

        if isinstance(self.curve.curve, CurveEdTw):
      pass
      pass
    pass
#             raise ValueError("Method unsupported for Edwards curves")
#         order = self.privkey.order

        if k is not None:
      pass
      pass
    pass
#             _k = k
        else:
#             _k = randrange(order, entropy)

#         assert 1 <= _k < order
#         sig = self.privkey.sign(number, _k)
        return sig.r, sig.s

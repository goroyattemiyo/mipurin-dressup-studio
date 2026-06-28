using UnityEngine;

namespace Mipurin.DressUp
{
    public class MipurinDressupController : MonoBehaviour
    {
        [Header("Sprite Renderers")]
        public SpriteRenderer hairBack;
        public SpriteRenderer wingLeft;
        public SpriteRenderer wingRight;
        public SpriteRenderer baseLayer;
        public SpriteRenderer outfit;
        public SpriteRenderer face;
        public SpriteRenderer eyes;
        public SpriteRenderer lipSync;
        public SpriteRenderer blush;
        public SpriteRenderer hairFront;
        public SpriteRenderer accessoryBody;
        public SpriteRenderer accessoryHead;
        public SpriteRenderer effectFront;

        [Header("Idle Motion")]
        public Transform floatRoot;
        public Transform hairFrontTransform;
        public Transform wingLeftTransform;
        public Transform wingRightTransform;

        public float floatAmplitude = 0.05f;
        public float floatSpeed = 1.2f;
        public float wingAmplitudeDegrees = 6.0f;
        public float wingSpeed = 2.5f;
        public float hairSwayDegrees = 1.5f;
        public float hairSwaySpeed = 1.0f;

        private Vector3 rootStartLocalPosition;
        private Quaternion wingLeftStartRotation;
        private Quaternion wingRightStartRotation;
        private Quaternion hairFrontStartRotation;

        private void Awake()
        {
            if (floatRoot == null) floatRoot = transform;
            rootStartLocalPosition = floatRoot.localPosition;
            if (wingLeftTransform != null) wingLeftStartRotation = wingLeftTransform.localRotation;
            if (wingRightTransform != null) wingRightStartRotation = wingRightTransform.localRotation;
            if (hairFrontTransform != null) hairFrontStartRotation = hairFrontTransform.localRotation;
        }

        private void Update()
        {
            ApplyFloatMotion();
            ApplyWingMotion();
            ApplyHairMotion();
        }

        private void ApplyFloatMotion()
        {
            if (floatRoot == null) return;
            float y = Mathf.Sin(Time.time * floatSpeed) * floatAmplitude;
            floatRoot.localPosition = rootStartLocalPosition + new Vector3(0f, y, 0f);
        }

        private void ApplyWingMotion()
        {
            float angle = Mathf.Sin(Time.time * wingSpeed) * wingAmplitudeDegrees;
            if (wingLeftTransform != null) wingLeftTransform.localRotation = wingLeftStartRotation * Quaternion.Euler(0f, 0f, angle);
            if (wingRightTransform != null) wingRightTransform.localRotation = wingRightStartRotation * Quaternion.Euler(0f, 0f, -angle);
        }

        private void ApplyHairMotion()
        {
            if (hairFrontTransform == null) return;
            float angle = Mathf.Sin(Time.time * hairSwaySpeed + 0.7f) * hairSwayDegrees;
            hairFrontTransform.localRotation = hairFrontStartRotation * Quaternion.Euler(0f, 0f, angle);
        }

        public void ApplyPart(MipurinPartItem item)
        {
            if (item == null) return;
            SetPartSprite(item.category, item.sprite);
        }

        public void SetPartSprite(MipurinPartCategory category, Sprite sprite)
        {
            SpriteRenderer target = GetRenderer(category);
            if (target == null) return;
            target.sprite = sprite;
        }

        public void ClearPart(MipurinPartCategory category)
        {
            SpriteRenderer target = GetRenderer(category);
            if (target == null) return;
            target.sprite = null;
        }

        private SpriteRenderer GetRenderer(MipurinPartCategory category)
        {
            switch (category)
            {
                case MipurinPartCategory.HairBack: return hairBack;
                case MipurinPartCategory.HairFront: return hairFront;
                case MipurinPartCategory.WingLeft: return wingLeft;
                case MipurinPartCategory.WingRight: return wingRight;
                case MipurinPartCategory.Base: return baseLayer;
                case MipurinPartCategory.Outfit: return outfit;
                case MipurinPartCategory.Face: return face;
                case MipurinPartCategory.Eyes: return eyes;
                case MipurinPartCategory.LipSync: return lipSync;
                case MipurinPartCategory.Blush: return blush;
                case MipurinPartCategory.AccessoryBody: return accessoryBody;
                case MipurinPartCategory.AccessoryHead: return accessoryHead;
                case MipurinPartCategory.EffectFront: return effectFront;
                default: return null;
            }
        }
    }
}

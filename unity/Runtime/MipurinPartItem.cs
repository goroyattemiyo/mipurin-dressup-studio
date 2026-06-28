using UnityEngine;

namespace Mipurin.DressUp
{
    [CreateAssetMenu(menuName = "Mipurin/DressUp Part Item")]
    public class MipurinPartItem : ScriptableObject
    {
        public string itemId;
        public string displayName;
        public MipurinPartCategory category;
        public Sprite sprite;
        public bool unlockedByDefault = true;
    }

    public enum MipurinPartCategory
    {
        HairBack,
        HairFront,
        WingLeft,
        WingRight,
        Base,
        Outfit,
        Face,
        Eyes,
        LipSync,
        Blush,
        AccessoryBody,
        AccessoryHead,
        EffectFront
    }
}

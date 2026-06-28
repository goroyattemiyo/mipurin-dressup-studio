using System.Collections;
using UnityEngine;

namespace Mipurin.DressUp
{
    public class MipurinTalkAnimator : MonoBehaviour
    {
        public SpriteRenderer eyesRenderer;
        public SpriteRenderer lipRenderer;
        public Sprite eyeOpen;
        public Sprite eyeClosed;
        public Sprite lipClose;
        public Sprite lipSmall;
        public Sprite lipOpen;

        public float blinkMinSeconds = 2.5f;
        public float blinkMaxSeconds = 5.5f;
        public float blinkClosedSeconds = 0.08f;
        public float talkFrameSeconds = 0.08f;

        private Coroutine blinkRoutine;
        private Coroutine talkRoutine;

        private void OnEnable()
        {
            blinkRoutine = StartCoroutine(BlinkLoop());
        }

        private void OnDisable()
        {
            if (blinkRoutine != null) StopCoroutine(blinkRoutine);
            if (talkRoutine != null) StopCoroutine(talkRoutine);
        }

        public void StartTalking(float seconds)
        {
            if (talkRoutine != null) StopCoroutine(talkRoutine);
            talkRoutine = StartCoroutine(TalkLoop(seconds));
        }

        private IEnumerator BlinkLoop()
        {
            while (true)
            {
                yield return new WaitForSeconds(Random.Range(blinkMinSeconds, blinkMaxSeconds));
                if (eyesRenderer != null && eyeClosed != null) eyesRenderer.sprite = eyeClosed;
                yield return new WaitForSeconds(blinkClosedSeconds);
                if (eyesRenderer != null && eyeOpen != null) eyesRenderer.sprite = eyeOpen;
            }
        }

        private IEnumerator TalkLoop(float seconds)
        {
            float end = Time.time + seconds;
            while (Time.time < end)
            {
                ApplyRandomLip();
                yield return new WaitForSeconds(talkFrameSeconds);
            }
            if (lipRenderer != null && lipClose != null) lipRenderer.sprite = lipClose;
        }

        private void ApplyRandomLip()
        {
            if (lipRenderer == null) return;
            int index = Random.Range(0, 3);
            if (index == 0 && lipClose != null) lipRenderer.sprite = lipClose;
            if (index == 1 && lipSmall != null) lipRenderer.sprite = lipSmall;
            if (index == 2 && lipOpen != null) lipRenderer.sprite = lipOpen;
        }
    }
}

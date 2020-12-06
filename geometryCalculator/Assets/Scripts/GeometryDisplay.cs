using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GeometryDisplay : MonoBehaviour
{
    [SerializeField]
    private Sprite _pointSprite = null;
    private LineRenderer _lr;

    private GameObject _pointsParent = null;

    private void Awake()
    {
        _lr = GetComponent<LineRenderer>();
    }

    private void Start()
    {
        _pointsParent = new GameObject("Points");
        _pointsParent.transform.parent = transform;
    }

    public void Cleanup()
    {
        _lr.positionCount = 0;

        foreach (Transform child in this.transform)
        {
            Destroy(child.gameObject);
        }
        _pointsParent = new GameObject("Points");
        _pointsParent.transform.parent = transform;
    }


    /// <summary>
    /// Adds a point to the current continoous line
    /// </summary>
    /// <param name="nextPoint"></param>
    public void ShowMainLine(Vector2 nextPoint)
    {
        _lr.positionCount++;
        _lr.SetPosition(_lr.positionCount - 1, nextPoint);
    }

    public void ShowLine(Vector2 p1, Vector2 p2, Color c)
    {
        GameObject lrgo = new GameObject("LineRenderer " + p1 + "    " + p2);
        lrgo.transform.parent = transform;

        lrgo.AddComponent<LineRenderer>();
        LineRenderer lr = lrgo.GetComponent<LineRenderer>();
        lr.positionCount = 2;
        lr.SetPosition(0, p1);
        lr.SetPosition(1, p2);
        lr.startColor = c;
        lr.endColor = c;

        lr.material = _lr.material;
        lr.startWidth = 0.15f;
        lr.endWidth = 0.15f;
    }

    public void ShowPoint(Vector2 pos, Color c, string name, float scale)
    {
        GameObject pgo = new GameObject(name);
        pgo.transform.parent = _pointsParent.transform;
        pgo.transform.position = pos;
        pgo.transform.localScale = new Vector3(scale, scale);

        pgo.AddComponent<SpriteRenderer>();
        SpriteRenderer sr = pgo.GetComponent<SpriteRenderer>();

        sr.sprite = _pointSprite;
        sr.color = c;
    }

    public void ShowTrackControlPoints(List<Vector2> controlPoints)
    {
        foreach(Vector2 c in controlPoints)
        {
            this.ShowMainLine(c);
        }
        this.ShowMainLine(controlPoints[0]);
    }
}

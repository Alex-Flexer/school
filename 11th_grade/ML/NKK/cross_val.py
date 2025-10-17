def kfold_split(n: int, k: int) -> list[tuple[list, list]]:
    fold_size = n // k
    idxs = list(range(n))
    return [
        (idxs[:i*fold_size] + idxs[(i+1) * fold_size:],
         idxs[i*fold_size:(i+1)*fold_size])
        for i in range(k)
    ]


def knn_cv_score(X, y, n_neighbors: int, metric, weights, normalizer, k: int, accuracy_score_function, knn_method) -> float:
    sum_scores = 0
    n = len(X)

    X_scaled = X
    if normalizer is not None:
        normalizer.fit(X, y)
        X_scaled = normalizer.transform(X)

    for idxs_train, idxs_test in kfold_split(n, k):
        clf = knn_method(
            n_neighbors,
            algorithm='brute',
            metric=metric,
            weights=weights
        )

        X_train = X_scaled[idxs_train]
        y_train = y[idxs_train]
        X_test = X_scaled[idxs_test]
        y_test = y[idxs_test]

        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        score = accuracy_score_function(y_test, y_pred)
        sum_scores += score

    return sum_scores / k

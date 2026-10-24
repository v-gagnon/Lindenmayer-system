module Main where

import System.Environment (getArgs)
import Data.List (isPrefixOf)
import Data.Maybe (fromMaybe)

type Rule = (Char, String)
type RuleTable = [Rule]

-- Nettoie les lignes vides et les commentaires (#)
cleanLines :: String -> [String]
cleanLines = filter (\l -> not (null l) && head l /= '#') . lines

-- Parse une ligne de règle
parseRule :: String -> Maybe Rule
parseRule line = case words line of
  [[c], "->", target] -> Just (c, target)
  _                   -> Nothing

-- Parse le fichier pour en extraire la seed et la liste de règles
parseFile :: String -> (String, RuleTable)
parseFile content = (seed, rules)
  where
    ls = cleanLines content
    
    seed = case filter ("seed:" `isPrefixOf`) ls of
      (s:_) -> dropWhile (== ' ') (drop 5 s)
      []    -> error "Erreur : aucune ligne 'seed:' trouvée dans le fichier."
    
    ruleLines = filter (not . ("seed:" `isPrefixOf`)) ls
    rules     = [r | Just r <- map parseRule ruleLines]

-- Applique une génération d'expansion déterministe
step :: RuleTable -> String -> String
step rules current = concatMap replace current
  where
    replace c = fromMaybe [c] (lookup c rules)

main :: IO ()
main = do
  args <- getArgs
  let (filepath, n) = case args of
        (f : k : _) -> (f, read k :: Int)
        [f]         -> (f, 5)
        []          -> ("rules/barnsley_fern.txt", 5)

  content <- readFile filepath
  let (seed, rules) = parseFile content

  let generations = take (n + 1) (iterate (step rules) seed)
  mapM_ putStrLn generations
from runner import Runner
from get_map import *
from common.arguments import get_common_args, get_coma_args, get_mixer_args, get_centralv_args, get_reinforce_args, get_commnet_args, get_g2anet_args


if __name__ == '__main__':
    for i in range(3):
        args = get_common_args()
        if args.alg.find('coma') > -1:
            args = get_coma_args(args)
        elif args.alg.find('central_v') > -1:
            args = get_centralv_args(args)
        elif args.alg.find('reinforce') > -1:
            args = get_reinforce_args(args)
        else:
            args = get_mixer_args(args)
        if args.alg.find('commnet') > -1:
            args = get_commnet_args(args)
        if args.alg.find('g2anet') > -1:
            args = get_g2anet_args(args)
        args.map = 'mapf' + str(i)
        env = potential()
        if args.load_model == True:
            env.show_animation = True

        # env.show_animation = True
        args.n_actions = 5
        args.n_agents = 2
        args.state_shape = 100
        args.obs_shape = 31
        args.episode_limit = 100

        args.obs_n = 1
        args.cover = 5
        args.n_epoch = 15001 #Train epoch
        args.save_cycle = 1000
        runner = Runner(env, args)
        if args.learn:
            runner.run(i)
        else:
            win_rate, _ = runner.evaluate()
            print('The win rate of {} is  {}'.format(args.alg, win_rate))
            break
